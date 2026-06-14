# the_gioi/vat_the/dan.py — Đạn + kiếm bay của boss và player
import pygame
import os as _os
from cai_dat import *

T = TILE_SIZE

# ── Gốc thư mục ──────────────────────────────────────────
_THU_MUC_GD = _os.path.dirname(
    _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

# ── Cache ảnh kiếm PNG (hướng dọc và ngang, có flip) ─────
_CACHE_KIEM_DAN = {}   # {(w, h, flip): Surface}

def _load_kiem_dan(w, h, flip=False):
    """Load kiem.png scale về (w,h). flip=True đổi chiều ngang."""
    key = (w, h, flip)
    if key in _CACHE_KIEM_DAN:
        return _CACHE_KIEM_DAN[key]
    path = _os.path.join(_THU_MUC_GD, 'tai_nguyen', 'hinh_anh', 'nhan_vat', 'kiem.png')
    if _os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (w, h))
            if flip:
                img = pygame.transform.flip(img, True, False)
            _CACHE_KIEM_DAN[key] = img
            return img
        except Exception:
            pass
    # Fallback
    s = _ve_kiem_bay(w, h, phase=1)
    if flip:
        s = pygame.transform.flip(s, True, False)
    _CACHE_KIEM_DAN[key] = s
    return s


# ── Cache ảnh tancong.png (vệt chém kiếm bay boss10 SK3) ─
_CACHE_TANCONG_DAN = {}   # {(w, h, flip): Surface}

def _load_tancong_dan(w, h, flip=False):
    """Load tancong.png scale về (w,h). flip=True đổi chiều ngang."""
    key = (w, h, flip)
    if key in _CACHE_TANCONG_DAN:
        return _CACHE_TANCONG_DAN[key]
    path = _os.path.join(_THU_MUC_GD, 'tai_nguyen', 'hinh_anh', 'nhan_vat', 'tancong.png')
    if _os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (w, h))
            if flip:
                img = pygame.transform.flip(img, True, False)
            _CACHE_TANCONG_DAN[key] = img
            return img
        except Exception:
            pass
    # Fallback
    s = _ve_kiem_bay(w, h, phase=2)
    if flip:
        s = pygame.transform.flip(s, True, False)
    _CACHE_TANCONG_DAN[key] = s
    return s


# ── Hàm vẽ fallback ──────────────────────────────────────
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
#  TIA BAN — chưởng boss5 SK3, kích thước 1×20 tile, xuyên tường
# ══════════════════════════════════════════════════════════
class TiaBan(pygame.sprite.Sprite):
    """
    Chưởng từ boss5 bắn về phía player.
    - Kích thước cố định: rộng T (1 tile), dài T*20 (20 tile).
    - Xoay theo góc boss → player.
    - Tâm đặt tại tâm boss, kéo dài về phía player.
    - Xuyên tường (không check va chạm tile).
    - Tồn tại FPS frame (1 giây), mờ dần ở 60% cuối.
    - Va chạm hitbox: hình chữ nhật theo góc thực (dùng mask).
    """
    SONG_TON  = FPS               # 60 frame = 1 giây
    MO_DAN_TU = int(FPS * 0.6)   # bắt đầu mờ từ frame 36
    DAI       = T * 20            # chiều dài 20 tile
    RONG      = T                 # chiều rộng 1 tile

    def __init__(self, bx, by, px, py):
        super().__init__()
        import math
        self._dem = 0
        self.chet = False

        # Tính góc boss → player
        dx = px - bx; dy = py - by
        self._goc = math.degrees(math.atan2(dy, dx))

        # Vẽ chưởng: W=DAI, H=RONG, xuất phát từ boss về phía player
        W = self.DAI; H = self.RONG
        surf = pygame.Surface((W, H), pygame.SRCALPHA)

        # Nền đỏ rực
        pygame.draw.rect(surf, (255, 50, 30, 230), (0, 0, W, H))
        # Viền sáng
        pygame.draw.rect(surf, (255, 160, 100, 200), (0, 2, W, H - 4))
        # Lõi trắng giữa
        pygame.draw.rect(surf, (255, 255, 200, 160), (0, H//2 - 2, W, 4))
        # Đầu chưởng sáng hơn
        pygame.draw.rect(surf, (255, 255, 255, 200), (W - 8, 0, 8, H))
        # Viền ngoài
        pygame.draw.rect(surf, (200, 30, 10, 255), (0, 0, W, H), 2)

        self._surf_goc = surf

        # Xoay theo góc
        self.image = pygame.transform.rotate(surf, -self._goc)

        # Đặt rect: cạnh trái (gốc) tại tâm boss, kéo dài về phía player
        # Trước khi xoay: gốc tọa độ là bx,by; rect kéo dài sang phải W pixel
        # Sau khi xoay: tính topleft từ tâm boss
        # Tâm của surf gốc trước xoay = (W//2, H//2) so với topleft
        # Điểm gốc (boss) = (0, H//2) trong surf gốc
        # Sau xoay, điểm đó di chuyển → tính lại
        rad = math.radians(self._goc)
        # Tâm surf gốc tại (W//2, H//2)
        # Điểm boss trong surf gốc: (0, H//2)
        # Vector từ tâm surf đến điểm boss: (-W//2, 0) → sau xoay:
        ox = -W // 2 * math.cos(rad) - 0 * math.sin(rad)
        oy = -W // 2 * (-math.sin(rad)) - 0 * math.cos(rad)
        # Tâm image sau xoay ứng với tâm surf gốc
        # Tâm image sau xoay: bx - ox_rotated, by - oy_rotated
        img_cx = bx - ox
        img_cy = by - oy
        self.rect = self.image.get_rect(center=(int(img_cx), int(img_cy)))

        # Mask để va chạm chính xác theo hình xoay
        self._mask = pygame.mask.from_surface(self.image)

        # Lưu vị trí boss để dùng khi cham_nguoi
        self._bx = bx; self._by = by

    def update(self, ds_nen=None):
        # Bắn xuyên — không cần check ds_nen
        self._dem += 1
        if self._dem >= self.MO_DAN_TU:
            tl = 1.0 - (self._dem - self.MO_DAN_TU) / max(
                1, self.SONG_TON - self.MO_DAN_TU)
            alpha = max(0, int(230 * tl))
            self.image = pygame.transform.rotate(self._surf_goc, -self._goc)
            self._mask = pygame.mask.from_surface(self.image)
            self.image.set_alpha(alpha)
        if self._dem >= self.SONG_TON:
            self.chet = True
            self.kill()

    def cham_nguoi(self, player_rect):
        """Va chạm dùng mask để chính xác với hình xoay."""
        if self.chet:
            return False
        # Kiểm tra rect trước cho nhanh
        if not self.rect.colliderect(player_rect):
            return False
        # Tạo mask nhân vật (hình chữ nhật đầy)
        p_mask = pygame.Mask(player_rect.size, fill=True)
        # Offset giữa 2 mask
        ox = player_rect.x - self.rect.x
        oy = player_rect.y - self.rect.y
        return bool(self._mask.overlap(p_mask, (ox, oy)))


# ══════════════════════════════════════════════════════════
#  QUẢ CẦU — đạn boss5 và boss10 SK1
# ══════════════════════════════════════════════════════════
import math as _math

_CACHE_CAU_LUA = None  # ảnh 60.png đã load

def _load_cau_lua():
    global _CACHE_CAU_LUA
    if _CACHE_CAU_LUA is not None:
        return _CACHE_CAU_LUA
    thu_muc_gd = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
    path = _os.path.join(thu_muc_gd, 'tai_nguyen', 'skill', 'cau_lua', '60.png')
    if _os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (T, T))
            _CACHE_CAU_LUA = img
            return img
        except Exception:
            pass
    # Fallback: vẽ tay
    s = pygame.Surface((T, T), pygame.SRCALPHA)
    pygame.draw.circle(s, (200, 80, 255), (T//2, T//2), T//2)
    pygame.draw.circle(s, (140, 40, 180), (T//2, T//2), T//2, 2)
    _CACHE_CAU_LUA = s
    return s


class QuaCau(pygame.sprite.Sprite):
    TOC_DO = 5

    SONG_TON = 8 * 60   # tồn tại tối đa 8 giây

    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        dx   = target_x - x
        dy   = target_y - y
        dist = max(1, (dx**2 + dy**2)**0.5)
        self._vx       = dx / dist * self.TOC_DO
        self._vy       = dy / dist * self.TOC_DO
        self._x        = float(x)
        self._y        = float(y)
        self._dem      = 0
        self._con_song = True   # dùng flag riêng, không phụ thuộc sprite group

        goc_bay        = _math.degrees(_math.atan2(dy, dx))
        self._goc_xoay = -(goc_bay + 90)

        surf_goc = _load_cau_lua()
        self.image     = pygame.transform.rotate(surf_goc, self._goc_xoay)
        self.rect      = self.image.get_rect(center=(int(x), int(y)))
        self._surf_goc = surf_goc

    def update(self, ds_nen=None):
        if not self._con_song:
            return
        self._dem += 1
        self._x += self._vx
        self._y += self._vy
        self.rect.center = (int(self._x), int(self._y))
        if self._dem >= self.SONG_TON:
            self._con_song = False
            self.kill()   # dọn khỏi group nếu có (boss5/10); no-op nếu chưa add group
            return
        if ds_nen:
            for n in ds_nen:
                if self.rect.colliderect(n.rect):
                    self._con_song = False
                    self.kill()
                    return

    def con_song(self):
        """Dùng thay alive() — không phụ thuộc sprite group."""
        return self._con_song

    def cham_nguoi(self, player_rect):
        if not self._con_song:
            return False
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
        # Dùng ảnh tancong.png: dọc nếu bay trên/dưới, ngang nếu bay trái/phải
        flip = dx < 0   # bay trái thì flip
        self.image = _load_tancong_dan(w, h, flip=flip)
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
        # Kiếm mưa rơi từ trên xuống → dọc 1×2
        self.image      = _load_kiem_dan(T, T*2, flip=False)
        self._surf_goc  = self.image.copy()
        self.rect       = self.image.get_rect(midtop=(x, y))
        self._x         = float(x); self._y = float(y)
        self._vx        = 0.0;      self._vy = 0.0
        self._spd       = 7 if phase == 1 else 11
        self._dem       = 0
        self._cham      = False
        self._cham_dem  = 0
        self._treo      = True   # đang lơ lửng trên không, chưa bay
        self._huong_luu = (0.0, 0.0)

    def dat_huong(self, tx, ty):
        dx = tx - self._x; dy = ty - self._y
        dist = max(1, (dx**2 + dy**2)**0.5)
        vx = dx / dist * self._spd
        vy = dy / dist * self._spd
        if self._treo:
            # Lưu hướng lại, chưa bay ngay
            self._huong_luu = (vx, vy)
        else:
            self._vx, self._vy = vx, vy

    def tha(self):
        """Bắt đầu rơi theo hướng đã lưu."""
        if self._treo:
            self._treo = False
            self._vx, self._vy = self._huong_luu

    def update(self, ds_nen=None):
        self._dem += 1
        if self._treo:
            return   # lơ lửng tại chỗ, không di chuyển, không tự hủy
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
        # KiemNem bay ngang 2×1 tile, flip theo hướng
        self.image = _load_kiem_dan(T*2, T, flip=(huong < 0))
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