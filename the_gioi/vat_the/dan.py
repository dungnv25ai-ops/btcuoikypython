# the_gioi/vat_the/dan.py — Đạn + kiếm bay của boss và player
import pygame
from cai_dat import *

T = TILE_SIZE

# ── Hàm vẽ dùng chung ────────────────────────────────────
_CACHE_CAU = None

def _ve_qua_cau(r=14):
    global _CACHE_CAU
    if _CACHE_CAU:
        return _CACHE_CAU.copy()
    s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
    pygame.draw.circle(s, (200, 80, 255), (r, r), r)
    pygame.draw.circle(s, (140, 40, 180), (r, r), r, 2)
    _CACHE_CAU = s
    return s.copy()


def _ve_kiem_bay(w, h, phase):
    s   = pygame.Surface((w, h), pygame.SRCALPHA)
    mau = (255, 80, 50) if phase == 2 else (255, 210, 20)
    pygame.draw.rect(s, mau,         (0, 0, w, h), border_radius=4)
    pygame.draw.rect(s, (180,130,0), (0, 0, w, h), 2, border_radius=4)
    return s


# ══════════════════════════════════════════════════════════
#  QUẢ CẦU — đạn boss5 và boss10 SK1
# ══════════════════════════════════════════════════════════
class QuaCau(pygame.sprite.Sprite):
    TOC_DO = 5

    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = _ve_qua_cau()
        self.rect  = self.image.get_rect(center=(x, y))
        self._x    = float(x); self._y = float(y)
        dx   = target_x - x; dy = target_y - y
        dist = max(1, (dx**2 + dy**2)**0.5)
        self._vx  = dx / dist * self.TOC_DO
        self._vy  = dy / dist * self.TOC_DO
        self._dem = 0

    def update(self, ds_nen=None):
        self._dem += 1
        self._x += self._vx; self._y += self._vy
        self.rect.center = (int(self._x), int(self._y))
        if ds_nen:
            for n in ds_nen:
                if self.rect.colliderect(n.rect):
                    self.kill(); return

    def cham_nguoi(self, player_rect):
        return self.rect.colliderect(player_rect)


# ══════════════════════════════════════════════════════════
#  KIẾM BAY — boss10 SK3
# ══════════════════════════════════════════════════════════
class KiemBay(pygame.sprite.Sprite):
    """Lướt thẳng 4 chiều, dính tường thì hết."""

    def __init__(self, x, y, dx, dy, phase=1):
        super().__init__()
        if dy != 0:
            w = T; h = T*2 if phase == 1 else T*3
        else:
            w = T*2 if phase == 1 else T*3; h = T
        self.image = _ve_kiem_bay(w, h, phase)
        self.rect  = self.image.get_rect(center=(x, y))
        self._x    = float(x); self._y = float(y)
        spd = 8 if phase == 1 else 13
        if abs(dx) >= abs(dy):
            self._vx = spd if dx > 0 else -spd; self._vy = 0
        else:
            self._vx = 0; self._vy = spd if dy > 0 else -spd
        self._dem = 0

    def update(self, ds_nen=None):
        self._dem += 1
        self._x += self._vx; self._y += self._vy
        self.rect.center = (int(self._x), int(self._y))
        if ds_nen:
            for n in ds_nen:
                if self.rect.colliderect(n.rect):
                    self.kill(); return
        if self._dem > 180:
            self.kill()

    def cham_nguoi(self, player_rect):
        return self.rect.colliderect(player_rect)


# ══════════════════════════════════════════════════════════
#  KIẾM MƯA — boss10 SK4
# ══════════════════════════════════════════════════════════
class KiemMua(pygame.sprite.Sprite):
    """Bay theo hướng đặt trước, sau khi chạm sàn có thể nhặt."""
    HIEN_SAU_CHAM = 300   # 5 giây

    def __init__(self, x, y, phase=1):
        super().__init__()
        self.image      = _ve_kiem_bay(T, T*2, phase)
        self._surf_goc  = self.image.copy()
        self.rect       = self.image.get_rect(midtop=(x, y))
        self._x         = float(x); self._y = float(y)
        self._vx        = 0.0;      self._vy = 0.0
        self._spd       = 7 if phase == 1 else 11
        self._dem       = 0
        self._cham      = False
        self._cham_dem  = 0

    def dat_huong(self, tx, ty):
        dx = tx - self._x; dy = ty - self._y
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
        self._x += self._vx; self._y += self._vy
        self.rect.center = (int(self._x), int(self._y))
        if ds_nen:
            for n in ds_nen:
                if self.rect.colliderect(n.rect):
                    self._cham = True; self._vx = self._vy = 0.0; return
        if self._dem > 10 * 60:
            self.kill()

    def cham_nguoi(self, player_rect):
        if self._cham: return False
        return self.rect.colliderect(player_rect)

    def co_the_nhat(self, player_rect):
        if not self._cham: return False
        return self.rect.inflate(8, 8).colliderect(player_rect)


# ══════════════════════════════════════════════════════════
#  KIẾM NÉM — skill F của người chơi
# ══════════════════════════════════════════════════════════
class KiemNem(pygame.sprite.Sprite):
    TOC_DO = 14

    def __init__(self, x, y, huong):
        super().__init__()
        w = T * 2; h = T
        self.image = _ve_kiem_bay(w, h, phase=2)
        if huong < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect  = self.image.get_rect(center=(x, y))
        self._x    = float(x)
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
        if self._dem > 6 * 60:
            self.kill()

    def cham_nguoi(self, r):
        return self.rect.colliderect(r)

    def cham_boss(self, boss_rect):
        return self.rect.colliderect(boss_rect)
