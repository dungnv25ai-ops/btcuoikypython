# the_gioi/vat_the/ke_di_chuyen.py — Kẻ địch di chuyển + đạn
import pygame
import math
import os as _os
from cai_dat import *

# ── Sprite animation loader ───────────────────────────────
_SPRITE_CACHE = {}

_DT_DI_CHUYEN = 1
_DT_TU_LUC    = 2
_DT_BAN       = 3
_DT_CHET      = 4


def _load_frames(dt_index):
    """Load 60 ảnh slimedt{dt_index:02d}{i:02d}.png, cache lại."""
    if dt_index in _SPRITE_CACHE:
        return _SPRITE_CACHE[dt_index]
    thu_muc = _os.path.join(
        _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))),
        "tai_nguyen")
    frames = []
    for i in range(1, 61):
        path = _os.path.join(thu_muc, f"slimedt{dt_index:02d}{i:02d}.png")
        if not _os.path.isfile(path):
            break
        try:
            img = pygame.image.load(path).convert_alpha()
            frames.append(pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)))
        except Exception:
            break
    _SPRITE_CACHE[dt_index] = frames
    return frames


def _ve_ke():
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(s, (160, 50, 180), (0, 0, TILE_SIZE, TILE_SIZE), border_radius=6)
    pygame.draw.rect(s, (120, 30, 140), (0, 0, TILE_SIZE, TILE_SIZE), 2, border_radius=6)
    return s


# ══════════════════════════════════════════════════════════
#  KHỐI ĐẠN — projectile của KeDiChuyen màn 6-9
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

    def alive(self):
        return self._alive

    def update(self, ds_nen=None):
        if not self._alive:
            return
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
        if not self._alive:
            return False
        return self.rect.colliderect(player_rect)


# ══════════════════════════════════════════════════════════
#  KẺ DI CHUYỂN
# ══════════════════════════════════════════════════════════
class KeDiChuyen(pygame.sprite.Sprite):
    """Kẻ 1x1 tuần tra. Màn 6-9: có skill bắn đạn."""
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
        self._surf_goc   = _ve_ke()
        self.image       = self._surf_goc.copy()
        self.rect        = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self._x          = float(self.rect.x)
        self.vel_x       = self.TOC_DO
        self.b_trai      = bien_gioi_trai * TILE_SIZE
        self.b_phai      = bien_gioi_phai * TILE_SIZE
        self.dem         = 0
        self._bien_mat   = False
        self._alpha      = 255
        self.mau         = 1
        self.co_tan_cong = co_tan_cong
        self._sk_cd      = self.HOI_CHIEU // 2
        self._sk_phase   = 0
        self._tu_luc_dem = 0
        self._huong_tc   = 1
        self._dan        = None
        self._anim_dt    = _DT_DI_CHUYEN
        self._anim_frame = 0
        self._anim_dem   = 0
        self._anim_spd   = 3
        self._frames     = {}
        self._ban_dem    = 0

    def _anim(self, dt, loop=True):
        if self._anim_dt != dt:
            self._anim_dt    = dt
            self._anim_frame = 0
            self._anim_dem   = 0

    def _tick_anim(self, loop=True):
        if self._anim_dt not in self._frames:
            self._frames[self._anim_dt] = _load_frames(self._anim_dt)
        frames = self._frames.get(self._anim_dt, [])
        if not frames:
            return self._surf_goc
        self._anim_dem += 1
        if self._anim_dem >= self._anim_spd:
            self._anim_dem = 0
            if loop:
                self._anim_frame = (self._anim_frame + 1) % len(frames)
            else:
                self._anim_frame = min(self._anim_frame + 1, len(frames) - 1)
        return frames[self._anim_frame]

    def _flip_img(self, surf):
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
            dx   = player_rect.centerx - self.rect.centerx
            dy   = player_rect.centery - self.rect.centery
            dist = max(1, (dx**2 + dy**2)**0.5)
            return True, int(dx/dist * self.LUC_DAY), int(dy/dist * self.LUC_DAY - 4)
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
            if self._alpha <= 0:
                self.kill()
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
                dang_tan_cong    = True
                self._tu_luc_dem += 1
                if player_rect:
                    self._huong_tc = 1 if player_rect.centerx >= self.rect.centerx else -1
                self._anim(_DT_TU_LUC)
                surf = self._tick_anim(loop=True)
                a    = int(160 + 95*abs(math.sin(self._tu_luc_dem * 0.25)))
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
            if self._anim_dt != _DT_BAN:
                self._anim(_DT_DI_CHUYEN)
            surf = self._tick_anim(loop=True)
            self.image = self._flip_img(surf)
