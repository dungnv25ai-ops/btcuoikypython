# the_gioi/vat_the/kiem.py — Kiếm vật phẩm + Sách mở Dash
import pygame
import math
import os as _os
from cai_dat import *

# ── Gốc thư mục ──────────────────────────────────────────
_THU_MUC_GD = _os.path.dirname(
    _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

# ── Load ảnh sách dùng chung ─────────────────────────────
_CACHE_SACH = None

def _load_anh_sach():
    global _CACHE_SACH
    if _CACHE_SACH is not None:
        return _CACHE_SACH
    path = _os.path.join(
        _THU_MUC_GD, 'tai_nguyen', 'hinh_anh', 'nhan_vat', 'sach.png')
    if _os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            _CACHE_SACH = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            return _CACHE_SACH
        except Exception:
            pass
    # Fallback vẽ tay
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(s, (30, 100, 200),  (2, 2, TILE_SIZE-4, TILE_SIZE-4), border_radius=5)
    pygame.draw.rect(s, (60, 140, 240),  (4, 4, TILE_SIZE-8, TILE_SIZE-8), border_radius=4)
    pygame.draw.rect(s, (240, 235, 200), (8, 6, TILE_SIZE-16, TILE_SIZE-10), border_radius=3)
    for i in range(3):
        pygame.draw.rect(s, (150, 140, 100), (10, 12+i*8, TILE_SIZE-22, 3))
    pygame.draw.rect(s, (20, 70, 160), (2, 2, 5, TILE_SIZE-4), border_radius=3)
    pygame.draw.rect(s, (15, 60, 140), (0, 0, TILE_SIZE, TILE_SIZE), 2, border_radius=5)
    _CACHE_SACH = s
    return _CACHE_SACH


# ── Load ảnh kiếm ─────────────────────────────────────────
_CACHE_KIEM_PNG = {}   # {(ngang, flip): Surface}

def _load_anh_kiem(ngang=False):
    """Load kiem.png, scale 1×2 tile dọc hoặc xoay 90° nếu ngang."""
    key = ngang
    if key in _CACHE_KIEM_PNG:
        return _CACHE_KIEM_PNG[key]

    path = _os.path.join(_THU_MUC_GD, 'tai_nguyen', 'hinh_anh', 'nhan_vat', 'kiem.png')
    if _os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            if ngang:
                # Xoay 90° ngược kim đồng hồ: chuôi sang trái, lưỡi sang phải
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE * 2))
                img = pygame.transform.rotate(img, 90)
                img = pygame.transform.scale(img, (TILE_SIZE * 2, TILE_SIZE))
            else:
                # Dọc: chuôi trên, lưỡi dưới — đúng như ảnh gốc
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE * 2))
            _CACHE_KIEM_PNG[key] = img
            return img
        except Exception:
            pass

    # Fallback vẽ tay
    return _ve_kiem(ngang)


# ── Vẽ kiếm fallback ──────────────────────────────────────
def _ve_kiem(ngang=False):
    W, H = (TILE_SIZE*2, TILE_SIZE) if ngang else (TILE_SIZE, TILE_SIZE*2)
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    pygame.draw.rect(s, (220, 200, 30), (0, 0, W, H), border_radius=4)
    pygame.draw.rect(s, (150, 120, 10), (0, 0, W, H), 2, border_radius=4)
    return s


class Kiem(pygame.sprite.Sprite):
    """Kiếm 1×2 tile — nhấn F khi gần để nhặt.
    Dùng ảnh tai_nguyen/hinh_anh/nhan_vat/kiem.png."""
    PHAM_VI = TILE_SIZE * 2

    def __init__(self, cot, hang, ngang=False):
        super().__init__()
        self.ngang       = ngang
        self.image       = _load_anh_kiem(ngang).copy()
        self.rect        = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self.dem_nhip    = 0
        self._alpha      = 255
        self._bien_mat   = False
        self._alpha_giam = 0
        self._surf_goc   = self.image.copy()   # giữ bản gốc để set_alpha đúng

    def gan_nguoi_choi(self, player_rect):
        return self.rect.inflate(self.PHAM_VI*2, self.PHAM_VI*2).colliderect(player_rect)

    def bat_dau_bien_mat(self):
        self._bien_mat   = True
        self._alpha_giam = 18

    def update(self):
        self.dem_nhip += 1
        if not self._bien_mat:
            a = int(220 + 35*math.sin(self.dem_nhip*0.08))
            self.image = self._surf_goc.copy()
            self.image.set_alpha(a)
        else:
            self._alpha = max(0, self._alpha - self._alpha_giam)
            self.image = self._surf_goc.copy()
            self.image.set_alpha(self._alpha)
            if self._alpha <= 0:
                self.kill()

    def ve_hint(self, screen, cam_x, cam_y, font):
        t  = font.render("[F] Nhat kiem", True, VANG)
        x  = self.rect.centerx - cam_x - t.get_width()//2
        y  = self.rect.top - cam_y - 22
        bg = pygame.Surface((t.get_width()+8, t.get_height()+4), pygame.SRCALPHA)
        pygame.draw.rect(bg, (0, 0, 0, 140), (0, 0, *bg.get_size()), border_radius=4)
        screen.blit(bg, (x-4, y-2))
        screen.blit(t, (x, y))


# ══════════════════════════════════════════════════════════
#  SÁCH VẬT PHẨM — nhặt mở Dash
# ══════════════════════════════════════════════════════════
class Sach1x1(pygame.sprite.Sprite):
    """Sách 1x1 — nhặt bằng F, mở khóa Dash.
    Dùng ảnh tai_nguyen/hinh_anh/nhan_vat/sach.png."""
    PHAM_VI = TILE_SIZE * 2

    def __init__(self, cot, hang):
        super().__init__()
        self.image     = _load_anh_sach().copy()
        self.rect      = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self.dem       = 0
        self._bien_mat = False
        self._alpha    = 255
        self._surf_goc = self.image.copy()

    def gan_nguoi_choi(self, player_rect):
        return self.rect.inflate(self.PHAM_VI*2, self.PHAM_VI*2).colliderect(player_rect)

    def bat_dau_bien_mat(self):
        self._bien_mat = True

    def update(self):
        self.dem += 1
        if not self._bien_mat:
            a = int(210 + 45*math.sin(self.dem*0.09))
            self.image = self._surf_goc.copy()
            self.image.set_alpha(a)
        else:
            self._alpha = max(0, self._alpha - 18)
            self.image = self._surf_goc.copy()
            self.image.set_alpha(self._alpha)
            if self._alpha <= 0:
                self.kill()

    def ve_hint(self, screen, cam_x, cam_y, font):
        t  = font.render("[F] Nhan sach: mo khoa Dash", True, (100, 200, 255))
        x  = self.rect.centerx - cam_x - t.get_width()//2
        y  = self.rect.top - cam_y - 22
        bg = pygame.Surface((t.get_width()+8, t.get_height()+4), pygame.SRCALPHA)
        pygame.draw.rect(bg, (0, 0, 0, 140), (0, 0, *bg.get_size()), border_radius=4)
        screen.blit(bg, (x-4, y-2))
        screen.blit(t, (x, y))


# ══════════════════════════════════════════════════════════
#  KIẾM CẦM TAY — hiển thị kiếm trên tay phải nhân vật
# ══════════════════════════════════════════════════════════
_CACHE_KIEM_CAM_TAY  = None
_CACHE_KIEM_CAM_FLIP = None

def _lay_anh_kiem_cam():
    global _CACHE_KIEM_CAM_TAY, _CACHE_KIEM_CAM_FLIP
    if _CACHE_KIEM_CAM_TAY is not None:
        return _CACHE_KIEM_CAM_TAY, _CACHE_KIEM_CAM_FLIP
    path = _os.path.join(_THU_MUC_GD, 'tai_nguyen', 'hinh_anh', 'nhan_vat', 'kiem.png')
    if _os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE ))
            
            # --- THÊM DÒNG NÀY ĐỂ XOAY KIẾM NGHIÊNG 45 ĐỘ ---
            img = pygame.transform.rotate(img, +135)
            _CACHE_KIEM_CAM_TAY  = img
            _CACHE_KIEM_CAM_FLIP = pygame.transform.flip(img, True, False)
            return _CACHE_KIEM_CAM_TAY, _CACHE_KIEM_CAM_FLIP
        except Exception:
            pass
    s = pygame.Surface((TILE_SIZE // 2, TILE_SIZE * 2), pygame.SRCALPHA)
    pygame.draw.rect(s, (200, 200, 220),
                     (s.get_width()//2-3, 0, 6, TILE_SIZE*2), border_radius=2)
    f = pygame.transform.flip(s, True, False)
    _CACHE_KIEM_CAM_TAY  = s
    _CACHE_KIEM_CAM_FLIP = f
    return s, f


class KiemCamTay:
    """Vẽ kiếm trên tay phải nhân vật. Ẩn khi di chuyển/leo/đánh."""

    def ve(self, screen, cam_x, cam_y, nhan_vat, hieu_ung=None):
        if not nhan_vat.co_danh:
            return

        dang_di   = nhan_vat.vel_x != 0
        dang_leo  = nhan_vat.dang_leo
        dang_dash = nhan_vat.dang_dash
        dang_danh = (hieu_ung is not None and hieu_ung.tan_cong.dang_danh)

        if dang_di or dang_leo or dang_dash or dang_danh:
            return

        anh_goc, anh_flip = _lay_anh_kiem_cam()
        pr = nhan_vat.rect
        
        if nhan_vat.huong == 1:
            anh = anh_goc
            # Hướng phải: Canh x lùi vào trong mép phải một chút để khớp tay
            x = pr.right - (TILE_SIZE // 1.5) - cam_x
        else:
            anh = anh_flip
            # Hướng trái: Canh x vừa qua mép trái
            x = pr.left - (TILE_SIZE // 4) - cam_x -20

        # Đẩy Y xuống thấp hơn một chút để ngang tầm tay (thay vì ngang đầu)
        y = pr.centery - (TILE_SIZE // 3) - cam_y - 30
        
        screen.blit(anh, (x, y))
