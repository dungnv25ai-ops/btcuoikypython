# the_gioi/boss.py
import pygame, math, os
from cai_dat import *

T = TILE_SIZE

# ══════════════════════════════════════════════════════════
#  Loader ảnh animation boss (giống KeDiChuyen)
#  Đọc từ tai_nguyen/hinh_anh/boss5/ và boss10/
#  Tên file: 1.png → N.png
# ══════════════════════════════════════════════════════════
_THU_MUC_GD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CACHE_FRAMES = {}   # {thu_muc_key: [Surface, ...]}

def _load_frames(thu_muc_con, so_luong=60):
    """Load ảnh 1.png→N.png từ tai_nguyen/hinh_anh/{thu_muc_con}/"""
    if thu_muc_con in _CACHE_FRAMES:
        return _CACHE_FRAMES[thu_muc_con]
    path = os.path.join(_THU_MUC_GD, 'tai_nguyen', 'hinh_anh', thu_muc_con)
    frames = []
    if os.path.isdir(path):
        for i in range(1, so_luong + 1):
            fp = os.path.join(path, f"{i}.png")
            if not os.path.isfile(fp):
                break
            try:
                img = pygame.image.load(fp).convert_alpha()
                img = pygame.transform.scale(img, (T*2, T*2))
                frames.append(img)
            except Exception:
                break
    _CACHE_FRAMES[thu_muc_con] = frames
    return frames


def _surf_du_phong(mau):
    """Surface dự phòng 2×2 tile khi không có ảnh."""
    s = pygame.Surface((T*2, T*2), pygame.SRCALPHA)
    pygame.draw.rect(s, mau, (0, 0, T*2, T*2), border_radius=6)
    pygame.draw.rect(s, (255, 255, 255, 80), (0, 0, T*2, T*2), 3, border_radius=6)
    return s


# ── Hằng số animation ────────────────────────────────────
ANIM_IDLE    = 'idle'
ANIM_TU_LUC  = 'tu_luc'
ANIM_BAN     = 'ban'
ANIM_BI_DANH = 'bi_danh'
ANIM_CHET    = 'chet'


# ══════════════════════════════════════════════════════════
#  Mixin animation chung cho Boss5 và Boss10
# ══════════════════════════════════════════════════════════
class BossAnimMixin:
    """
    Mixin cung cấp hệ thống animation cho boss.
    Class con cần khai báo:
        _THU_MUC_ANIM = {'idle': 'boss5/idle', 'tu_luc': 'boss5/tu_luc', ...}
        _SPD = 2   # mỗi ảnh hiện bao nhiêu frame game (30fps = 2)
    """
    _SPD = 2

    def _anim_init(self):
        self._anim_hien  = ANIM_IDLE
        self._anim_frame = 0
        self._anim_dem   = 0
        self._anim_loop  = True    # True = loop, False = play 1 lần rồi giữ frame cuối
        self._anim_xong  = False   # True khi play 1 lần xong

    def _anim_doi(self, ten, loop=True):
        """Chuyển animation, reset frame nếu khác."""
        if self._anim_hien != ten:
            self._anim_hien  = ten
            self._anim_frame = 0
            self._anim_dem   = 0
            self._anim_loop  = loop
            self._anim_xong  = False

    def _anim_tick(self):
        """Cập nhật frame, trả về Surface hiện tại."""
        ten    = self._anim_hien
        thu_mc = self._THU_MUC_ANIM.get(ten, '')
        frames = _load_frames(thu_mc) if thu_mc else []

        if not frames:
            return self._surf_du_phong

        self._anim_dem += 1
        if self._anim_dem >= self._SPD:
            self._anim_dem = 0
            if self._anim_loop:
                self._anim_frame = (self._anim_frame + 1) % len(frames)
            else:
                if self._anim_frame < len(frames) - 1:
                    self._anim_frame += 1
                else:
                    self._anim_xong = True
        return frames[self._anim_frame]


# ══════════════════════════════════════════════════════════
#  BOSS 5
# ══════════════════════════════════════════════════════════
class Boss5(BossAnimMixin, pygame.sprite.Sprite):
    """Boss màn 5 — sống sót 60s. Ký hiệu '5' trên map."""
    TU_LUC_TIME  = 120
    BAN_COOLDOWN = 180

    _THU_MUC_ANIM = {
        ANIM_IDLE   : 'boss5/idle',
        ANIM_TU_LUC : 'boss5/tu_luc',
        ANIM_BAN    : 'boss5/ban',
        ANIM_BI_DANH: 'boss5/bi_danh',
        ANIM_CHET   : 'boss5/chet',
    }

    def __init__(self, cot, hang):
        pygame.sprite.Sprite.__init__(self)
        self._surf_du_phong = _surf_du_phong((180, 50, 220))
        self._anim_init()
        self.image = self._surf_du_phong
        # Đặt chân boss sát đất tại ô (cot, hang)
        self.rect  = self.image.get_rect(midbottom=(cot*T + T//2, hang*T + T))
        self._dem     = 0
        self._ban_cd  = self.BAN_COOLDOWN
        self._tu_luc  = 0
        self.can_ban  = False

    def update(self):
        self._dem += 1

        if self._tu_luc > 0:
            self._tu_luc -= 1
            self._anim_doi(ANIM_TU_LUC, loop=True)
            if self._tu_luc == 0:
                self.can_ban = True
                self._anim_doi(ANIM_BAN, loop=False)
        elif self._anim_hien == ANIM_BAN and self._anim_xong:
            self._anim_doi(ANIM_IDLE, loop=True)
        elif self._anim_hien not in (ANIM_TU_LUC, ANIM_BAN, ANIM_BI_DANH, ANIM_CHET):
            self._anim_doi(ANIM_IDLE, loop=True)

        if self._ban_cd > 0 and self._tu_luc == 0:
            self._ban_cd -= 1

        surf = self._anim_tick()
        self.image = surf

    def cham_nguoi(self, player_rect):
        return False

    def ve_thanh_thoi_gian(self, screen, cam_x, cam_y, con_lai, font):
        sx, sy = self.rect.centerx - cam_x, self.rect.top - cam_y - 24
        BW, BH = 120, 12
        bx = sx - BW//2
        pygame.draw.rect(screen, (30,30,30), (bx,sy,BW,BH), border_radius=5)
        tl  = max(0, con_lai / 60)
        mau = (50,200,50) if tl > 0.4 else (220,160,0) if tl > 0.2 else (220,50,50)
        pygame.draw.rect(screen, mau, (bx,sy,int(BW*tl),BH), border_radius=5)
        pygame.draw.rect(screen, (180,180,180), (bx,sy,BW,BH), 1, border_radius=5)
        t = font.render(f"{int(con_lai)}s", True, TRANG)
        screen.blit(t, t.get_rect(center=(sx, sy-12)))


# ══════════════════════════════════════════════════════════
#  BOSS 10
# ══════════════════════════════════════════════════════════
class Boss10(BossAnimMixin, pygame.sprite.Sprite):
    """Boss màn 10 — 2 phase, 10+20 HP. Ký hiệu '1' trên map."""
    SO_MAU_MAX   = 10
    TU_LUC_TIME  = 90
    BAN_COOLDOWN = 120

    _THU_MUC_ANIM = {
        ANIM_IDLE        : 'boss10/idle_p1',
        'idle_p2'        : 'boss10/idle_p2',
        ANIM_TU_LUC      : 'boss10/tu_luc',
        ANIM_BAN         : 'boss10/ban',
        'teleport_di'    : 'boss10/teleport_di',
        'teleport_den'   : 'boss10/teleport_den',
        'chem'           : 'boss10/chem',
        'ne'             : 'boss10/ne',
        'enrage'         : 'boss10/enrage',
        ANIM_BI_DANH     : 'boss10/bi_danh',
        ANIM_CHET        : 'boss10/chet',
    }

    def __init__(self, cot, hang):
        pygame.sprite.Sprite.__init__(self)
        self._surf_du_phong = _surf_du_phong((200, 30, 30))
        self._anim_init()
        self.image      = self._surf_du_phong
        self.rect       = self.image.get_rect(midbottom=(cot*T + T//2, hang*T + T))
        self._dem       = 0
        self._ban_cd    = self.BAN_COOLDOWN
        self._tu_luc    = 0
        self.can_ban    = False
        self.mau        = self.SO_MAU_MAX
        self._flash     = 0
        self._phase     = 1   # phase hiện tại (để chọn idle đúng)

    def nhan_don(self):
        if self.mau <= 0:
            return True
        self.mau -= 1
        self._flash = 14
        self._anim_doi(ANIM_BI_DANH, loop=False)
        return self.mau <= 0

    def da_chet(self):
        return self.mau <= 0

    def cham_nguoi(self, player_rect):
        return False

    def update(self):
        self._dem += 1

        # Ưu tiên: chet > flash/bi_danh > tu_luc > ban > idle
        if self.da_chet():
            self._anim_doi(ANIM_CHET, loop=False)
            surf = self._anim_tick()
            cur  = self.image.get_alpha() or 255
            self.image = surf
            self.image.set_alpha(max(0, cur - 8))
            if cur <= 8:
                self.kill()
            return

        # Hết bi_danh → về idle
        if self._anim_hien == ANIM_BI_DANH and self._anim_xong:
            self._flash = 0
            idle = 'idle_p2' if self._phase == 2 else ANIM_IDLE
            self._anim_doi(idle, loop=True)

        # Flash nháy trắng (vẫn chạy song song với animation)
        if self._flash > 0:
            self._flash -= 1

        if self._tu_luc > 0:
            self._tu_luc -= 1
            self._anim_doi(ANIM_TU_LUC, loop=True)
            if self._tu_luc == 0:
                self.can_ban = True
                self._anim_doi(ANIM_BAN, loop=False)
        elif self._anim_hien == ANIM_BAN and self._anim_xong:
            idle = 'idle_p2' if self._phase == 2 else ANIM_IDLE
            self._anim_doi(idle, loop=True)
        elif self._anim_hien not in (
                ANIM_TU_LUC, ANIM_BAN, ANIM_BI_DANH, ANIM_CHET,
                'teleport_di', 'teleport_den', 'chem', 'ne', 'enrage'):
            idle = 'idle_p2' if self._phase == 2 else ANIM_IDLE
            self._anim_doi(idle, loop=True)

        if self._ban_cd > 0 and self._tu_luc == 0:
            self._ban_cd -= 1

        surf = self._anim_tick()
        # Nháy trắng khi bị đánh
        if self._flash > 0:
            surf = surf.copy()
            surf.fill((255, 255, 255, 120), special_flags=pygame.BLEND_RGBA_ADD)
        self.image = surf

    def ve_thanh_mau(self, screen, cam_x, cam_y, font):
        if self.da_chet():
            return
        sx, sy = self.rect.centerx - cam_x, self.rect.top - cam_y - 24
        BW, BH = 130, 14
        bx = sx - BW//2
        pygame.draw.rect(screen, (40,10,10), (bx,sy,BW,BH), border_radius=5)
        tl = self.mau / self.SO_MAU_MAX
        pygame.draw.rect(screen, (200,30,30), (bx,sy,int(BW*tl),BH), border_radius=5)
        pygame.draw.rect(screen, (220,150,150), (bx,sy,BW,BH), 1, border_radius=5)
        for i in range(1, self.SO_MAU_MAX):
            vx = bx + int(BW * i / self.SO_MAU_MAX)
            pygame.draw.line(screen, (0,0,0), (vx,sy), (vx,sy+BH), 2)
        t = font.render(f"BOSS {self.mau}/{self.SO_MAU_MAX}", True, TRANG)
        screen.blit(t, t.get_rect(center=(sx, sy-12)))