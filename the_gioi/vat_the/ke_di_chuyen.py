# the_gioi/vat_the/ke_di_chuyen.py — Kẻ địch di chuyển + đạn
import pygame
import math
import os as _os
from cai_dat import *

# ── Gốc thư mục tài nguyên ───────────────────────────────
_THU_MUC_GD = _os.path.dirname(
    _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

# ── Cache: {loai_quai: (surf_goc, surf_flip)} ────────────
_CACHE_ANH = {}

# ── Cache animation cầu lửa tụ lực (1-60.png) ───────────
_CACHE_CAU_LUA_ANIM = []

def _load_cau_lua_anim():
    global _CACHE_CAU_LUA_ANIM
    if _CACHE_CAU_LUA_ANIM:
        return _CACHE_CAU_LUA_ANIM
    thu_muc = _os.path.join(_THU_MUC_GD, 'tai_nguyen', 'skill', 'cau_lua')
    for i in range(1, 61):
        path = _os.path.join(thu_muc, f"{i}.png")
        if not _os.path.isfile(path):
            break
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            _CACHE_CAU_LUA_ANIM.append(img)
        except Exception:
            pass
    return _CACHE_CAU_LUA_ANIM


def _loai_quai_tu_man(so_man):
    if 1 <= so_man <= 4:
        return 'quai1'
    return 'quai2'


def _load_anh(loai_quai):
    """Load 1 ảnh PNG, trả về (surf_goc, surf_flip). Cache lại."""
    if loai_quai in _CACHE_ANH:
        return _CACHE_ANH[loai_quai]

    path = _os.path.join(
        _THU_MUC_GD, 'tai_nguyen', 'hinh_anh', f'{loai_quai}.png')
    if _os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            result = (img, pygame.transform.flip(img, True, False))
            _CACHE_ANH[loai_quai] = result
            return result
        except Exception:
            pass

    # Fallback
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(s, (160, 50, 180), (0, 0, TILE_SIZE, TILE_SIZE), border_radius=6)
    pygame.draw.rect(s, (120, 30, 140), (0, 0, TILE_SIZE, TILE_SIZE), 2, border_radius=6)
    result = (s, pygame.transform.flip(s, True, False))
    _CACHE_ANH[loai_quai] = result
    return result


# ══════════════════════════════════════════════════════════
#  KHỐI ĐẠN
# ══════════════════════════════════════════════════════════
class _KhoiDan(pygame.sprite.Sprite):
    TOC_DO = 6

    def __init__(self, x, y, tx, ty):
        super().__init__()
        T = TILE_SIZE
        s = pygame.Surface((T, T), pygame.SRCALPHA)
        pygame.draw.rect(s, (220, 60, 60, 220),  (0, 0, T, T), border_radius=6)
        pygame.draw.rect(s, (255, 100, 100, 200), (2, 2, T-4, T//3), border_radius=4)
        pygame.draw.rect(s, (255, 50, 50, 255),   (0, 0, T, T), 2, border_radius=6)
        self.image  = s
        self.rect   = self.image.get_rect(center=(x, y))
        self._x     = float(x); self._y = float(y)
        dx = tx - x; dy = ty - y
        dist = max(1, (dx**2 + dy**2)**0.5)
        self._vx    = dx / dist * self.TOC_DO
        self._vy    = dy / dist * self.TOC_DO
        self._dem   = 0
        self._alive = True

    def alive(self): return self._alive

    def update(self, ds_nen=None):
        if not self._alive: return
        self._dem += 1
        self._x += self._vx; self._y += self._vy
        self.rect.center = (int(self._x), int(self._y))
        if ds_nen:
            for n in ds_nen:
                if self.rect.colliderect(n.rect):
                    self._alive = False; return
        if self._dem > 8 * 60:
            self._alive = False

    def cham_nguoi(self, player_rect):
        if not self._alive: return False
        return self.rect.colliderect(player_rect)


# ══════════════════════════════════════════════════════════
#  KẺ DI CHUYỂN
# ══════════════════════════════════════════════════════════
class KeDiChuyen(pygame.sprite.Sprite):
    TOC_DO       = 1.5
    NHAY_BIEN_DO = 0.5
    NHAY_TOC_DO  = 0.05
    PHAM_VI_DAY  = TILE_SIZE * 1
    PHAM_VI_DIET = TILE_SIZE * 2
    LUC_DAY      = 12
    I_FRAMES     = 40
    TAM_DANH     = 10 * TILE_SIZE
    TU_LUC_TIME  = 1 * 60   # 1 giây tụ lực
    HOI_CHIEU    = 1 * 60   # 1 giây hồi chiêu sau khi bắn

    def __init__(self, cot, hang, bien_gioi_trai, bien_gioi_phai,
                 co_tan_cong=False, so_man=1):
        super().__init__()
        self._loai_quai  = _loai_quai_tu_man(so_man)
        self._surf_goc, self._surf_flip = _load_anh(self._loai_quai)
        self.image       = self._surf_goc
        self.rect        = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self._x          = float(self.rect.x)
        self._y_goc      = float(self.rect.y)
        self._nhay_dem   = 0
        self.vel_x       = self.TOC_DO
        self.b_trai      = bien_gioi_trai * TILE_SIZE
        self.b_phai      = bien_gioi_phai * TILE_SIZE
        self.dem         = 0
        self._bien_mat   = False
        self._alpha      = 255
        self.mau         = 1
        self.co_tan_cong = co_tan_cong
        self._sk_phase   = 0   # 0=chờ/hồi chiêu, 1=tụ lực, 2=đạn đang bay
        self._tu_luc_dem = 0
        self._hoi_chieu  = 0   # đếm hồi chiêu sau khi bắn
        self._huong_tc   = 1
        self._dan        = None

    def _lay_anh(self, flip=False):
        return self._surf_flip if flip else self._surf_goc

    def _flip_can(self):
        if self._sk_phase == 1:
            return self._huong_tc < 0
        return self.vel_x < 0

    def gan_nguoi_choi(self, player_rect):
        if self._sk_phase == 1: return False
        return self.rect.inflate(self.PHAM_VI_DIET*2, self.PHAM_VI_DIET*2)\
                   .colliderect(player_rect)

    def kiem_tra_tan_cong(self, player_rect, i_frames):
        if self._bien_mat or i_frames > 0 or self._sk_phase == 1:
            return False, 0, 0
        if self.rect.colliderect(player_rect):
            dx   = player_rect.centerx - self.rect.centerx
            dy   = player_rect.centery - self.rect.centery
            dist = max(1, (dx**2 + dy**2)**0.5)
            return True, int(dx/dist * self.LUC_DAY), int(dy/dist * self.LUC_DAY - 4)
        return False, 0, 0

    def bat_dau_bien_mat(self): self._bien_mat = True

    def nhan_don(self):
        self.mau -= 1
        if self.mau <= 0:
            self._bien_mat = True
            return True
        return False

    def update(self, ds_nen_tang, player_rect=None):
        self.dem += 1

        # ── Đang biến mất ────────────────────────────────
        if self._bien_mat:
            self._alpha = max(0, self._alpha - 20)
            surf = self._lay_anh(self._flip_can()).copy()
            surf.set_alpha(self._alpha)
            self.image = surf
            if self._alpha <= 0:
                self.kill()
            return

        # ── Update đạn — lọc KhoiTanHinh để đạn không chạm khối tàng hình ──
        if self._dan is not None:
            from the_gioi.nen_tang import KhoiTanHinh
            ds_dac = [n for n in ds_nen_tang if not isinstance(n, KhoiTanHinh)]
            self._dan.update(ds_dac)
            da_tat = not self._dan.con_song() if hasattr(self._dan, 'con_song') \
                     else not self._dan.alive()
            if da_tat:
                self._dan = None
                # Đạn tắt → bắt đầu đếm hồi chiêu 1 giây
                if self._sk_phase == 2:
                    self._sk_phase  = 0
                    self._hoi_chieu = self.HOI_CHIEU

        # ── Đếm hồi chiêu ────────────────────────────────
        if self._hoi_chieu > 0:
            self._hoi_chieu -= 1

        # ── Skill tấn công ───────────────────────────────
        dang_tan_cong = False
        if self.co_tan_cong and player_rect is not None:

            # Phase 0: chờ hồi chiêu xong rồi mới tụ lực
            if self._sk_phase == 0 and self._hoi_chieu <= 0:
                dx = player_rect.centerx - self.rect.centerx
                dy = player_rect.centery - self.rect.centery
                if abs(dx) <= self.TAM_DANH and abs(dy) <= self.TAM_DANH:
                    self._sk_phase   = 1
                    self._tu_luc_dem = 0
                    self._huong_tc   = 1 if dx >= 0 else -1

            # Phase 1: tụ lực 1 giây — đứng yên, xoay theo player
            elif self._sk_phase == 1:
                dang_tan_cong    = True
                self._tu_luc_dem += 1
                # Luôn cập nhật hướng nhìn theo player trong lúc tụ lực
                self._huong_tc = 1 if player_rect.centerx >= self.rect.centerx else -1

                # Animation cầu lửa
                frames = _load_cau_lua_anim()
                if frames:
                    tl  = min(1.0, self._tu_luc_dem / self.TU_LUC_TIME)
                    idx = min(int(tl * len(frames)), len(frames) - 1)
                    surf = self._lay_anh(self._huong_tc < 0).copy()
                    lua  = frames[idx]
                    lx   = surf.get_width() // 2 - lua.get_width() // 2
                    W    = surf.get_width()
                    H    = surf.get_height() + lua.get_height()
                    combined = pygame.Surface((W, H), pygame.SRCALPHA)
                    combined.blit(lua,  (lx, 0))
                    combined.blit(surf, (0,  lua.get_height()))
                    self.image = combined
                    self.rect  = self.image.get_rect(
                        midbottom=(int(self._x) + TILE_SIZE // 2,
                                   int(self._y_goc) + TILE_SIZE))
                else:
                    a = int(160 + 95*abs(math.sin(self._tu_luc_dem * 0.25)))
                    surf = self._lay_anh(self._huong_tc < 0).copy()
                    surf.set_alpha(a)
                    self.image = surf

                # Tụ lực xong → bắn
                if self._tu_luc_dem >= self.TU_LUC_TIME:
                    from the_gioi.vat_the.dan import QuaCau
                    bx = self.rect.centerx
                    by = self.rect.centery - TILE_SIZE // 2
                    px = player_rect.centerx
                    py = player_rect.centery
                    self._dan        = QuaCau(bx, by, px, py)
                    self._sk_phase   = 2
                    self._tu_luc_dem = 0   # reset để lần sau tụ lực lại từ đầu
                    self.vel_x       = self.TOC_DO * self._huong_tc
                    self.image       = self._lay_anh(self._huong_tc < 0)
                    self.rect        = self.image.get_rect(
                        midbottom=(int(self._x) + TILE_SIZE // 2,
                                   int(self._y_goc) + TILE_SIZE))
                return  # không di chuyển khi tụ lực

            # Phase 2: đạn đang bay — tiếp tục di chuyển bình thường
            # (phase về 0 khi đạn tắt, xử lý ở phần update đạn bên trên)

        # ── Di chuyển ngang ───────────────────────────────
        if not dang_tan_cong:
            self._x += self.vel_x
            self.rect.x = int(self._x)
            dung_tuong = False
            for n in ds_nen_tang:
                if self.rect.colliderect(n.rect):
                    dung_tuong = True
                    if self.vel_x > 0:  self.rect.right = n.rect.left
                    elif self.vel_x < 0: self.rect.left = n.rect.right
                    self._x = float(self.rect.x); break
            co_dat_do = False
            rc = pygame.Rect(
                self.rect.right+2 if self.vel_x > 0 else self.rect.left-4,
                self.rect.bottom+2, 2, 2)
            for n in ds_nen_tang:
                if rc.colliderect(n.rect): co_dat_do = True; break
            if (dung_tuong or not co_dat_do
                    or self._x <= self.b_trai
                    or self._x >= self.b_phai - self.rect.width):
                self.vel_x *= -1
                if self._x <= self.b_trai:
                    self._x = float(self.b_trai); self.vel_x = abs(self.TOC_DO)
                elif self._x >= self.b_phai - self.rect.width:
                    self._x = float(self.b_phai - self.rect.width)
                    self.vel_x = -abs(self.TOC_DO)
                self.rect.x = int(self._x)

            self._nhay_dem += 1
            dy_sin = math.sin(self._nhay_dem * self.NHAY_TOC_DO) * self.NHAY_BIEN_DO
            self.rect.y = int(self._y_goc + dy_sin)

            self.image = self._lay_anh(self.vel_x < 0)