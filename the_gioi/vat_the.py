# the_gioi/vat_the.py — Các vật thể đặc biệt: Kiếm, Kẻ di chuyển
import pygame
import math, math, random
from cai_dat import *

# ══════════════════════════════════════════════════════════
#  KIẾM — 1x2 dọc, màu vàng, nhấn F để nhặt
# ══════════════════════════════════════════════════════════
def _ve_kiem(ngang=False):
    W,H=(TILE_SIZE*2,TILE_SIZE) if ngang else (TILE_SIZE,TILE_SIZE*2)
    s=pygame.Surface((W,H),pygame.SRCALPHA)
    pygame.draw.rect(s,(220,200,30),(0,0,W,H),border_radius=4)
    pygame.draw.rect(s,(150,120,10),(0,0,W,H),2,border_radius=4)
    return s

class Kiem(pygame.sprite.Sprite):
    """Kiếm 1x2 — nhấn F khi gần để nhặt (biến mất)."""
    PHAM_VI = TILE_SIZE * 2   # khoảng cách nhặt

    def __init__(self, cot, hang, ngang=False):
        super().__init__()
        self.ngang   = ngang
        self.image   = _ve_kiem(ngang)
        self.rect    = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self.dem_nhip= 0
        self._alpha  = 255
        self._bien_mat = False
        self._alpha_giam = 0

    def gan_nguoi_choi(self, player_rect):
        return self.rect.inflate(self.PHAM_VI*2, self.PHAM_VI*2)\
                   .colliderect(player_rect)

    def bat_dau_bien_mat(self):
        self._bien_mat  = True
        self._alpha_giam = 18

    def update(self):
        self.dem_nhip += 1
        # Nhấp nháy nhẹ khi chờ
        if not self._bien_mat:
            a = int(220 + 35*math.sin(self.dem_nhip*0.08))
            self.image.set_alpha(a)
        else:
            self._alpha = max(0, self._alpha - self._alpha_giam)
            self.image.set_alpha(self._alpha)
            if self._alpha <= 0:
                self.kill()

    def ve_hint(self, screen, cam_x, cam_y, font):
        """Hiện chữ [F] phía trên kiếm."""
        t = font.render("[F] Nhặt kiếm", True, VANG)
        x = self.rect.centerx - cam_x - t.get_width()//2
        y = self.rect.top      - cam_y - 22
        bg = pygame.Surface((t.get_width()+8,t.get_height()+4),pygame.SRCALPHA)
        pygame.draw.rect(bg,(0,0,0,140),(0,0,*bg.get_size()),border_radius=4)
        screen.blit(bg,(x-4,y-2)); screen.blit(t,(x,y))


# ══════════════════════════════════════════════════════════
#  KẺ DI CHUYỂN — 1x1, đi qua nhân vật, chuột trái để diệt
# ══════════════════════════════════════════════════════════
def _ve_ke():
    s=pygame.Surface((TILE_SIZE,TILE_SIZE),pygame.SRCALPHA)
    pygame.draw.rect(s,(160,50,180),(0,0,TILE_SIZE,TILE_SIZE),border_radius=6)
    pygame.draw.rect(s,(120,30,140),(0,0,TILE_SIZE,TILE_SIZE),2,border_radius=6)
    return s

# ── Loader sprite sheet animation ────────────────────────
import os as _os
_SPRITE_CACHE = {}   # {dt_index: [Surface, ...]}

def _load_frames(dt_index):
    """Load 60 ảnh slimedt{dt_index:02d}{i:02d}.png, cache lại."""
    if dt_index in _SPRITE_CACHE:
        return _SPRITE_CACHE[dt_index]
    thu_muc = _os.path.join(
        _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
        "tai_nguyen")
    frames = []
    for i in range(1, 61):
        ten = f"slimedt{dt_index:02d}{i:02d}.png"
        path = _os.path.join(thu_muc, ten)
        if not _os.path.isfile(path):
            break
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            frames.append(img)
        except Exception:
            break
    _SPRITE_CACHE[dt_index] = frames
    return frames

# Chỉ số dt cho từng trạng thái
_DT_DI_CHUYEN = 1
_DT_TU_LUC    = 2
_DT_BAN       = 3
_DT_CHET      = 4


class KeDiChuyen(pygame.sprite.Sprite):
    """Kẻ 1x1: đẩy + kill người chơi khi chạm.
    Màn 6-9: thêm skill bắn khối 1x1 vào player, hồi chiêu 10s.
    Sprite animation: dùng ảnh nếu có, fallback vẽ nếu không."""
    TOC_DO       = 1.5
    PHAM_VI_DAY  = TILE_SIZE * 1
    PHAM_VI_DIET = TILE_SIZE * 2
    LUC_DAY      = 12
    I_FRAMES     = 40

    TAM_DANH     = 10 * TILE_SIZE
    TU_LUC_TIME  = 5 * 60
    HOI_CHIEU    = 10 * 60

    def __init__(self, cot, hang, bien_gioi_trai, bien_gioi_phai, co_tan_cong=False):
        super().__init__()
        self._surf_goc = _ve_ke()
        self.image    = self._surf_goc.copy()
        self.rect     = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self._x       = float(self.rect.x)
        self.vel_x    = self.TOC_DO
        self.b_trai   = bien_gioi_trai * TILE_SIZE
        self.b_phai   = bien_gioi_phai * TILE_SIZE
        self.dem      = 0
        self._bien_mat= False
        self._alpha   = 255
        self.mau      = 1   # HP mặc định
        # Skill
        self.co_tan_cong = co_tan_cong
        self._sk_cd      = self.HOI_CHIEU // 2
        self._sk_phase   = 0
        self._tu_luc_dem = 0
        self._huong_tc   = 1
        self._dan        = None
        # Animation — frames load lazy khi vẽ lần đầu
        self._anim_dt    = _DT_DI_CHUYEN
        self._anim_frame = 0
        self._anim_dem   = 0
        self._anim_spd   = 3
        self._frames     = {}   # load lazy trong _tick_anim
        self._ban_dem    = 0

    def _anim(self, dt, loop=True):
        """Chuyển sang animation dt, hoặc giữ nếu đang dùng."""
        if self._anim_dt != dt:
            self._anim_dt    = dt
            self._anim_frame = 0
            self._anim_dem   = 0

    def _tick_anim(self, loop=True):
        """Cập nhật frame animation, trả về Surface hiện tại."""
        # Lazy load
        if self._anim_dt not in self._frames:
            self._frames[self._anim_dt] = _load_frames(self._anim_dt)
        frames = self._frames.get(self._anim_dt, [])
        if not frames:
            return self._surf_goc   # fallback

        self._anim_dem += 1
        if self._anim_dem >= self._anim_spd:
            self._anim_dem = 0
            if loop:
                self._anim_frame = (self._anim_frame + 1) % len(frames)
            else:
                self._anim_frame = min(self._anim_frame + 1, len(frames) - 1)
        return frames[self._anim_frame]

    def _flip_img(self, surf):
        """Lật ngang nếu đang đi trái."""
        if self.vel_x < 0 or self._huong_tc < 0:
            return pygame.transform.flip(surf, True, False)
        return surf

    def gan_nguoi_choi(self, player_rect):
        if self._sk_phase == 1:
            return False
        return self.rect.inflate(self.PHAM_VI_DIET*2, self.PHAM_VI_DIET*2)\
                   .colliderect(player_rect)

    def kiem_tra_tan_cong(self, player_rect, i_frames):
        if self._bien_mat or i_frames > 0 or self._sk_phase == 1:
            return False, 0, 0
        if self.rect.colliderect(player_rect):
            dx = player_rect.centerx - self.rect.centerx
            dy = player_rect.centery - self.rect.centery
            dist = max(1, (dx**2+dy**2)**0.5)
            day_x = int(dx/dist * self.LUC_DAY)
            day_y = int(dy/dist * self.LUC_DAY - 4)
            return True, day_x, day_y
        return False, 0, 0

    def bat_dau_bien_mat(self):
        self._bien_mat = True

    def nhan_don(self):
        self.mau -= 1
        if self.mau <= 0:
            self._bien_mat = True
            return True
        return False

    def update(self, ds_nen_tang, player_rect=None):
        self.dem += 1

        if self._bien_mat:
            self._anim(_DT_CHET)
            surf = self._tick_anim(loop=False)
            self._alpha = max(0, self._alpha - 20)
            surf = surf.copy(); surf.set_alpha(self._alpha)
            self.image = surf
            if self._alpha <= 0: self.kill()
            return

        if self._dan is not None:
            self._dan.update(ds_nen_tang)
            if not self._dan.alive():
                self._dan = None

        dang_tan_cong = False
        if self.co_tan_cong and player_rect is not None:
            if self._sk_phase == 0:
                if self._sk_cd > 0:
                    self._sk_cd -= 1
                else:
                    dx = player_rect.centerx - self.rect.centerx
                    dy = player_rect.centery - self.rect.centery
                    if abs(dx) <= self.TAM_DANH and abs(dy) <= self.TAM_DANH:
                        self._sk_phase   = 1
                        self._tu_luc_dem = 0
                        self._huong_tc   = 1 if dx >= 0 else -1
            elif self._sk_phase == 1:
                dang_tan_cong = True
                self._tu_luc_dem += 1
                if player_rect:
                    self._huong_tc = 1 if player_rect.centerx >= self.rect.centerx else -1
                self._anim(_DT_TU_LUC)
                surf = self._tick_anim(loop=True)
                a = int(160 + 95*abs(math.sin(self._tu_luc_dem * 0.25)))
                surf = surf.copy(); surf.set_alpha(a)
                self.image = self._flip_img(surf)
                if self._tu_luc_dem >= self.TU_LUC_TIME:
                    bx = self.rect.centerx; by = self.rect.top - TILE_SIZE
                    px = player_rect.centerx if player_rect else bx + self._huong_tc*100
                    py = player_rect.centery if player_rect else by
                    self._dan      = _KhoiDan(bx, by, px, py)
                    self._sk_phase = 2
                    self._sk_cd    = self.HOI_CHIEU
                    self.vel_x     = self.TOC_DO * self._huong_tc
                    self._anim(_DT_BAN); self._ban_dem = 0
                return
            elif self._sk_phase == 2:
                self._sk_cd -= 1
                if self._sk_cd <= 0:
                    self._sk_phase = 0; self._sk_cd = 0
                if self._anim_dt == _DT_BAN:
                    self._ban_dem += 1
                    frames = self._frames.get(_DT_BAN, [])
                    if frames and self._ban_dem >= len(frames)*self._anim_spd:
                        self._anim(_DT_DI_CHUYEN)

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
            import pygame as _pg
            rc = _pg.Rect(self.rect.right+2 if self.vel_x>0 else self.rect.left-4,
                          self.rect.bottom+2, 2, 2)
            for n in ds_nen_tang:
                if rc.colliderect(n.rect): co_dat_do = True; break
            if dung_tuong or not co_dat_do or self._x <= self.b_trai or self._x >= self.b_phai - self.rect.width:
                self.vel_x *= -1
                if self._x <= self.b_trai:
                    self._x = float(self.b_trai); self.vel_x = abs(self.TOC_DO)
                elif self._x >= self.b_phai - self.rect.width:
                    self._x = float(self.b_phai-self.rect.width)
                    self.vel_x = -abs(self.TOC_DO)
                self.rect.x = int(self._x)
            if self._anim_dt != _DT_BAN:
                self._anim(_DT_DI_CHUYEN)
            surf = self._tick_anim(loop=True)
            self.image = self._flip_img(surf)


class _KhoiDan(pygame.sprite.Sprite):
    """Khối đạn của KeDiChuyen màn 6-9."""
    TOC_DO = 6

def __init__(self, x, y, tx, ty):
    super().__init__()
    T = TILE_SIZE
    s = pygame.Surface((T, T), pygame.SRCALPHA)
    pygame.draw.rect(s, (220, 60, 60, 220), (0,0,T,T), border_radius=6)
    pygame.draw.rect(s, (255,100,100,200), (2,2,T-4,T//3), border_radius=4)
    pygame.draw.rect(s, (255,50,50,255), (0,0,T,T), 2, border_radius=6)
    self.image = s
    self.rect  = self.image.get_rect(center=(x, y))
    self._x    = float(x); self._y = float(y)
    dx = tx - x; dy = ty - y
    dist = max(1, (dx**2+dy**2)**0.5)
    self._vx = dx/dist * self.TOC_DO
    self._vy = dy/dist * self.TOC_DO
    self._dem = 0
    self._alive = True
    self.add(pygame.sprite.Group())   # cần group để alive() hoạt động

def alive(self):
    return self._alive

def update(self, ds_nen=None):
    if not self._alive: return
    self._dem += 1
    self._x += self._vx; self._y += self._vy
    self.rect.center = (int(self._x), int(self._y))
    if ds_nen:
        for n in ds_nen:
            if self.rect.colliderect(n.rect):
                self._alive = False; return
    if self._dem > 8*60: self._alive = False

def cham_nguoi(self, player_rect):
    if not self._alive: return False
    return self.rect.colliderect(player_rect)

# ══════════════════════════════════════════════════════════
#  SÁCH 1x1 — nhấn F để nhặt, mở khóa kỹ năng lướt
# ══════════════════════════════════════════════════════════
def _ve_sach():
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    # Bìa sách xanh
    pygame.draw.rect(s,(30,100,200),(2,2,TILE_SIZE-4,TILE_SIZE-4),border_radius=5)
    pygame.draw.rect(s,(60,140,240),(4,4,TILE_SIZE-8,TILE_SIZE-8),border_radius=4)
    # Trang giấy
    pygame.draw.rect(s,(240,235,200),(8,6,TILE_SIZE-16,TILE_SIZE-10),border_radius=3)
    # Chữ trên trang (3 dòng giả)
    for i in range(3):
        y = 12 + i*8
        pygame.draw.rect(s,(150,140,100),(10,y,TILE_SIZE-22,3))
    # Gáy sách
    pygame.draw.rect(s,(20,70,160),(2,2,5,TILE_SIZE-4),border_radius=3)
    # Biểu tượng chớp (kỹ năng)
    pts = [(TILE_SIZE-14,8),(TILE_SIZE-8,20),(TILE_SIZE-13,20),(TILE_SIZE-7,TILE_SIZE-8)]
    pygame.draw.polygon(s,(255,230,50),pts)
    pygame.draw.polygon(s,(200,170,20),pts,1)
    pygame.draw.rect(s,(15,60,140),(0,0,TILE_SIZE,TILE_SIZE),2,border_radius=5)
    return s

class Sach1x1(pygame.sprite.Sprite):
    """Sách 1x1 — nhặt bằng F, mở khóa dash."""
    PHAM_VI = TILE_SIZE * 2

    def __init__(self, cot, hang):
        super().__init__()
        self.image    = _ve_sach()
        self.rect     = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self.dem      = 0
        self._bien_mat= False
        self._alpha   = 255

    def gan_nguoi_choi(self, player_rect):
        return self.rect.inflate(self.PHAM_VI*2, self.PHAM_VI*2).colliderect(player_rect)

    def bat_dau_bien_mat(self):
        self._bien_mat = True

    def update(self):
        self.dem += 1
        if not self._bien_mat:
            a = int(210 + 45*math.sin(self.dem*0.09))
            self.image.set_alpha(a)
        else:
            self._alpha = max(0, self._alpha - 18)
            self.image.set_alpha(self._alpha)
            if self._alpha <= 0: self.kill()

    def ve_hint(self, screen, cam_x, cam_y, font):
        t = font.render("[F] Nhan sach: mo khoa Dash", True, (100,200,255))
        x = self.rect.centerx - cam_x - t.get_width()//2
        y = self.rect.top - cam_y - 22
        bg = pygame.Surface((t.get_width()+8,t.get_height()+4),pygame.SRCALPHA)
        pygame.draw.rect(bg,(0,0,0,140),(0,0,*bg.get_size()),border_radius=4)
        screen.blit(bg,(x-4,y-2)); screen.blit(t,(x,y))


# ══════════════════════════════════════════════════════════
#  KHỐI DỊCH CHUYỂN 2x2 — chạm vào → teleport
# ══════════════════════════════════════════════════════════
def _ve_khoi_dc():
    W, H = TILE_SIZE*2, TILE_SIZE*2
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    # Nền tím
    pygame.draw.rect(s,(100,30,180),(0,0,W,H),border_radius=8)
    pygame.draw.rect(s,(140,70,220),(2,2,W-4,H-4),border_radius=7)
    # Vòng xoáy/portal
    cx,cy = W//2, H//2
    for r,a,c in [(36,255,(200,150,255)),(28,200,(180,120,255)),(20,160,(160,100,240))]:
        surf_c = pygame.Surface((r*2,r*2),pygame.SRCALPHA)
        pygame.draw.circle(surf_c,c+(a,),(r,r),r)
        s.blit(surf_c,(cx-r,cy-r))
    pygame.draw.circle(s,(255,255,255,230),(cx,cy),8)
    # Tia sáng
    for ang in range(0,360,45):
        rad = math.radians(ang)
        x1=int(cx+12*math.cos(rad)); y1=int(cy+12*math.sin(rad))
        x2=int(cx+22*math.cos(rad)); y2=int(cy+22*math.sin(rad))
        pygame.draw.line(s,(220,180,255,180),(x1,y1),(x2,y2),2)
    # Viền
    pygame.draw.rect(s,(180,100,255),(0,0,W,H),3,border_radius=8)
    return s

_CACHE_GAI = _CACHE_NUOC = _CACHE_CAU = None

def _ve_gai():
    global _CACHE_GAI
    if _CACHE_GAI is not None: return _CACHE_GAI.copy()
    
    T = TILE_SIZE
    try:
        # Load ảnh
        img = pygame.image.load("tai_nguyen/khoi/gai.png").convert_alpha()
        
        # CHỈNH KÍCH THƯỚC Ở ĐÂY:
        # Ép ảnh vừa khít ô TxT. 
        # Nếu bạn muốn gai cao hơn bình thường, bạn có thể chỉnh (T, int(T*1.2)) 
        # nhưng (T, T) là chuẩn nhất để không đè lên ô khác.
        s = pygame.transform.scale(img, (T, T))
        
    except Exception as e:
        # Nếu lỗi ảnh, dùng code vẽ dự phòng của bạn
        s = pygame.Surface((T, T), pygame.SRCALPHA)
        pygame.draw.rect(s, (40, 40, 40), (0, T//2, T, T//2))
        for i in range(4):
            x = int(T/8 + i*T/4)
            pygame.draw.polygon(s, (160, 160, 160), [(x-T//10, T), (x+T//10, T), (x, T//4)])
            pygame.draw.polygon(s, (220, 220, 220), [(x-T//14, T-4), (x+T//14, T-4), (x, T//4+4)])
            
    _CACHE_GAI = s
    return s.copy()
def _ve_nuoc(dem=0):
    global _CACHE_NUOC
    T = TILE_SIZE
    s = pygame.Surface((T,T), pygame.SRCALPHA)
    pygame.draw.rect(s,(30,100,200,160),(0,0,T,T))
    pygame.draw.rect(s,(100,180,255,255),(0,0,T,T),1)
    if _CACHE_NUOC is None: _CACHE_NUOC = True
    return s

def _ve_qua_cau(r=14):
    global _CACHE_CAU
    if _CACHE_CAU: return _CACHE_CAU.copy()
    s = pygame.Surface((r*2,r*2), pygame.SRCALPHA)
    pygame.draw.circle(s,(200,80,255),(r,r),r)
    pygame.draw.circle(s,(140,40,180),(r,r),r,2)
    _CACHE_CAU = s
    return s.copy()

class Gai(pygame.sprite.Sprite):
    """Gai nhọn đứng im, chạm vào là mất mạng. Hitbox đã được thu nhỏ ở man_choi"""
    def __init__(self, cot, hang):
        super().__init__()
        # Gọi hàm vẽ gai (đảm bảo hàm _ve_gai của bạn không còn tham số roi)
        self.image = _ve_gai() 
        self.rect = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
    def kiem_tra_cham_nguoi(self, player_rect):
        return self.rect.colliderect(player_rect)
class KhoiDichChuyen(pygame.sprite.Sprite):
    """Khối teleport. Mặc định 2x2."""
    def __init__(self, cot, hang, dich_den_cot=42, dich_den_hang=5, rong=2, cao=2):
        super().__init__()
        W = TILE_SIZE*rong; H = TILE_SIZE*cao
        s = pygame.Surface((W,H),pygame.SRCALPHA)
        # Vẽ portal
        pygame.draw.rect(s,(100,30,180),(0,0,W,H),border_radius=8)
        pygame.draw.rect(s,(140,70,220),(2,2,W-4,H-4),border_radius=7)
        cx,cy=W//2,H//2
        for r,a,c in [(min(W,H)//2-4,200,(200,150,255)),(min(W,H)//2-10,180,(180,120,255))]:
            gs=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
            pygame.draw.circle(gs,c+(a,),(r,r),r)
            s.blit(gs,(cx-r,cy-r))
        pygame.draw.circle(s,(255,255,255,220),(cx,cy),6)
        import math as _m
        for ang in range(0,360,60):
            rd=_m.radians(ang)
            x1=int(cx+10*_m.cos(rd)); y1=int(cy+10*_m.sin(rd))
            x2=int(cx+18*_m.cos(rd)); y2=int(cy+18*_m.sin(rd))
            pygame.draw.line(s,(220,180,255,160),(x1,y1),(x2,y2),2)
        pygame.draw.rect(s,(180,100,255),(0,0,W,H),3,border_radius=8)
        self._surf_orig    = s
        self.image         = self._surf_orig.copy()
        self.rect          = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self.dem           = 0
        self.dich_cot      = dich_den_cot
        self.dich_hang     = dich_den_hang
        # Vị trí cổng (để biết chiều teleport)
        self._cot_cong     = cot
        self._hang_cong    = hang
        # Hội thoại cổng
        self._trong_vung   = False   # player đang trong vùng
        self._hoi_thoai_hien = False  # đang hiện hội thoại
        self._cho_tra_loi  = False   # đang chờ Y/N
        self.font          = None

    def _init_font(self):
        if not self.font:
            self.font = pygame.font.SysFont(FONT_CHINH, 16)

    def update(self):
        self.dem += 1
        a = int(180+75*abs(math.sin(self.dem*0.06)))
        self.image = self._surf_orig.copy()
        self.image.set_alpha(a)

    def xu_ly_vung(self, player_rect):
        """Gọi mỗi frame. Trả về True nếu cần hiện hội thoại lần đầu."""
        dang_trong = self.rect.inflate(TILE_SIZE,TILE_SIZE).colliderect(player_rect)
        if dang_trong and not self._trong_vung:
            # Vừa bước vào
            self._hoi_thoai_hien = True
            self._cho_tra_loi    = True
        if not dang_trong and self._trong_vung:
            # Bước ra → reset để hiện lại lần sau
            self._hoi_thoai_hien = False
            self._cho_tra_loi    = False
        self._trong_vung = dang_trong
        return self._hoi_thoai_hien

    def tra_loi_co(self, player_rect=None):
        """Người chơi chọn Có → trả về tọa độ đích.
        Nếu player ở bên phải cổng → teleport về cot_cong-3 (chiều ngược).
        Nếu player ở bên trái cổng → teleport đến dich_cot (chiều tiến).
        """
        self._hoi_thoai_hien = False
        self._cho_tra_loi    = False
        if player_rect is not None:
            # Player bên phải cổng → đi ngược về
            if player_rect.centerx > (self._cot_cong + 2) * TILE_SIZE:
                return ((self._cot_cong - 3) * TILE_SIZE, self.dich_hang * TILE_SIZE)
        return (self.dich_cot * TILE_SIZE, self.dich_hang * TILE_SIZE)

    def tra_loi_khong(self):
        """Người chơi chọn Không → đóng hội thoại, KHÔNG teleport."""
        self._hoi_thoai_hien = False
        self._cho_tra_loi    = False

    def ve_hoi_thoai(self, screen, cam_x, cam_y, mw, mh):
        if not self._hoi_thoai_hien: return
        self._init_font()
        font_to = pygame.font.SysFont(FONT_CHINH, 18, bold=True)
        cx = self.rect.centerx - cam_x
        cy = self.rect.top     - cam_y - 10

        BW, BH = 300, 100
        bx = max(8, min(cx-BW//2, mw-BW-8))
        by = max(8, cy-BH-10)

        bong = pygame.Surface((BW,BH),pygame.SRCALPHA)
        pygame.draw.rect(bong,(20,10,40,230),(0,0,BW,BH),border_radius=10)
        pygame.draw.rect(bong,(180,100,255,255),(0,0,BW,BH),2,border_radius=10)
        screen.blit(bong,(bx,by))

        t1 = font_to.render("Ban co muon di vao khong?",True,(220,180,255))
        screen.blit(t1,t1.get_rect(center=(bx+BW//2,by+28)))

        # Nút Y / N
        for i,(lbl,mau) in enumerate([("Y  Co",(80,200,80)),("N  Khong",(200,80,80))]):
            rr = pygame.Rect(bx+30+i*150, by+58, 110, 30)
            mx,my2=pygame.mouse.get_pos()
            hv=rr.collidepoint(mx,my2)
            pygame.draw.rect(screen,tuple(min(c+40,255) for c in mau) if hv else mau,rr,border_radius=6)
            t2=self.font.render(lbl,True,TRANG)
            screen.blit(t2,t2.get_rect(center=rr.center))

        # Lưu rect nút để bắt click
        self._rect_co   = pygame.Rect(bx+30,  by+58, 110, 30)
        self._rect_khong= pygame.Rect(bx+180, by+58, 110, 30)

    def xu_ly_click_hoi_thoai(self, ev_pos):
        """Trả về 'co', 'khong', hoặc None."""
        if not self._cho_tra_loi: return None
        if hasattr(self,'_rect_co')   and self._rect_co.collidepoint(ev_pos):   return 'co'
        if hasattr(self,'_rect_khong') and self._rect_khong.collidepoint(ev_pos): return 'khong'
        return None


# ══════════════════════════════════════════════════════════
#  KHỐI RƠI — 1x2 ngang hoặc dọc, rơi từ trên, chạm = chết
# ══════════════════════════════════════════════════════════
def _ve_khoi_roi(ngang=False):
    W,H=(TILE_SIZE*2,TILE_SIZE) if ngang else (TILE_SIZE,TILE_SIZE)
    s=pygame.Surface((W,H),pygame.SRCALPHA)
    pygame.draw.rect(s,(180,100,30),(0,0,W,H),border_radius=4)
    pygame.draw.rect(s,(120,60,10),(0,0,W,H),2,border_radius=4)
    return s

class KhoiNuoc(pygame.sprite.Sprite):
    """Khối nước 1x1 — đứng trong = giảm tốc, bơi lên bằng Space/W."""
    def __init__(self, cot, hang):
        super().__init__()
        self._dem   = 0
        self._cot   = cot
        self._hang  = hang
        self.image  = _ve_nuoc(0)
        self.rect   = self.image.get_rect(topleft=(cot * TILE_SIZE, hang * TILE_SIZE))

    def update(self):
        self._dem += 1
        # Vẽ lại với frame mới để animate sóng
        if self._dem % 4 == 0:
            self.image = _ve_nuoc(self._dem)


class QuaCau(pygame.sprite.Sprite):
    """Quả cầu bắn thẳng từ boss đến player."""
    TOC_DO = 5

    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = _ve_qua_cau()
        self.rect  = self.image.get_rect(center=(x,y))
        self._x    = float(x); self._y = float(y)
        dx = target_x - x; dy = target_y - y
        dist = max(1,(dx**2+dy**2)**0.5)
        self._vx = dx/dist*self.TOC_DO
        self._vy = dy/dist*self.TOC_DO
        self._dem = 0

    def update(self, ds_nen=None):
        self._dem += 1
        self._x += self._vx; self._y += self._vy
        self.rect.center = (int(self._x), int(self._y))
        # Chỉ mất khi chạm tường
        if ds_nen:
            for n in ds_nen:
                if self.rect.colliderect(n.rect):
                    self.kill(); return

    def cham_nguoi(self, player_rect):
        return self.rect.colliderect(player_rect)


# ── Kiếm bay (Skill 3 boss10) ─────────────────────────────
def _ve_kiem_bay(w, h, phase):
    s=pygame.Surface((w,h),pygame.SRCALPHA)
    mau=(255,80,50) if phase==2 else (255,210,20)
    pygame.draw.rect(s,mau,(0,0,w,h),border_radius=4)
    pygame.draw.rect(s,(180,130,0),(0,0,w,h),2,border_radius=4)
    return s


class KiemBay(pygame.sprite.Sprite):
    """Kiếm bay từ boss10 skill3 — lướt thẳng, dính tường thì hết."""
    def __init__(self, x, y, dx, dy, phase=1):
        super().__init__()
        T = TILE_SIZE
        # Phase1: 1x2, Phase2: 1x3
        if dy != 0: w = T; h = T*2 if phase==1 else T*3
        else:       w = T*2 if phase==1 else T*3; h = T

        self.image = _ve_kiem_bay(w, h, phase)
        self.rect  = self.image.get_rect(center=(x, y))
        self._x    = float(x); self._y = float(y)
        spd = 8 if phase==1 else 13
        # Chuẩn hóa hướng (4 chiều)
        if abs(dx) >= abs(dy):
            self._vx = spd if dx>0 else -spd; self._vy = 0
        else:
            self._vx = 0; self._vy = spd if dy>0 else -spd
        self._dem = 0

    def update(self, ds_nen=None):
        self._dem += 1
        self._x += self._vx; self._y += self._vy
        self.rect.center = (int(self._x), int(self._y))
        # Dính tường → hết
        if ds_nen:
            for n in ds_nen:
                if self.rect.colliderect(n.rect):
                    self.kill(); return
        # Tự xóa sau 3s
        if self._dem > 180: self.kill()

    def cham_nguoi(self, player_rect):
        return self.rect.colliderect(player_rect)


# ── Kiếm mưa (SK4 boss10) ─────────────────────────────────
class KiemMua(pygame.sprite.Sprite):
    """Kiếm 1×2 từ boss, bay thẳng theo hướng đã định khi spawn.
    Sau khi chạm tường/sàn: hiện 1s rồi biến mất (có thể nhặt)."""
    def __init__(self, x, y, phase=1):
        super().__init__()
        T = TILE_SIZE
        self.image = _ve_kiem_bay(T, T*2, phase)
        self._surf_goc = self.image.copy()
        self.rect  = self.image.get_rect(midtop=(x, y))
        self._x    = float(x)
        self._y    = float(y)
        self._vx   = 0.0
        self._vy   = 0.0
        self._spd  = 7 if phase == 1 else 11
        self._dem  = 0
        self._cham = False
        self._cham_dem = 0
        self.HIEN_SAU_CHAM = 300  # 5 giây

    def dat_huong(self, tx, ty):
        """Gọi 1 lần sau khi tạo để set hướng bay thẳng về target."""
        dx = tx - self._x
        dy = ty - self._y
        dist = max(1, (dx**2 + dy**2)**0.5)
        self._vx = dx / dist * self._spd
        self._vy = dy / dist * self._spd

    def update(self, ds_nen=None):
        self._dem += 1
        if self._cham:
            self._cham_dem += 1
            alpha = int(255 * (1.0 - self._cham_dem / self.HIEN_SAU_CHAM))
            self.image = self._surf_goc.copy()
            self.image.set_alpha(max(0, alpha))
            if self._cham_dem >= self.HIEN_SAU_CHAM:
                self.kill()
            return
        self._x += self._vx
        self._y += self._vy
        self.rect.center = (int(self._x), int(self._y))
        if ds_nen:
            for n in ds_nen:
                if self.rect.colliderect(n.rect):
                    self._cham = True
                    self._vx = self._vy = 0.0
                    return
        if self._dem > 10 * 60: self.kill()

    def cham_nguoi(self, player_rect):
        if self._cham: return False
        return self.rect.colliderect(player_rect)

    def co_the_nhat(self, player_rect):
        """Chỉ nhặt được khi đã chạm sàn (_cham=True)."""
        if not self._cham:
            return False
        return self.rect.inflate(8, 8).colliderect(player_rect)


# ── Kiếm ném (skill F người chơi) ─────────────────────────
class KiemNem(pygame.sprite.Sprite):
    """Kiếm ném thẳng theo hướng nhân vật, dính tường thì hết."""
    TOC_DO = 14

    def __init__(self, x, y, huong):
        super().__init__()
        T = TILE_SIZE
        # Ngang theo hướng ném
        w = T * 2; h = T
        self.image = _ve_kiem_bay(w, h, phase=2)
        if huong < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect  = self.image.get_rect(center=(x, y))
        self._x    = float(x)
        self._y    = float(y)
        self._vx   = float(self.TOC_DO * huong)
        self._dem  = 0

    def update(self, ds_nen=None):
        self._dem += 1
        self._x += self._vx
        self.rect.centerx = int(self._x)
        if ds_nen:
            for n in ds_nen:
                if self.rect.colliderect(n.rect):
                    self.kill(); return
        if self._dem > 6 * 60: self.kill()   # timeout 6s

    def cham_nguoi(self, r):
        return self.rect.colliderect(r)

    def cham_boss(self, boss_rect):
        return self.rect.colliderect(boss_rect)
