# the_gioi/hieu_ung.py — Hiệu ứng xấu lên người chơi
# ============================================================
#  HieuUngTroiChan:
#    - Tổng 5 giây:
#        0.0s → 2.0s : animation 1→60  (xuất hiện)
#        2.0s → 3.0s : giữ frame 60    (duy trì)
#        3.0s → 5.0s : animation 60→1  (biến mất)
#    - Khóa player giây 1.0s → 4.0s (3 giây ở giữa)
#    - Chiếm 1×1 tile dưới chân người chơi
#    - Cấm: di chuyển, nhảy, dash, đánh, ném
#    - Cho phép: Q (hoán đổi / giáp bất tử)
# ============================================================

import pygame
import os
from cai_dat import *

T = TILE_SIZE

# ── Loader ảnh ───────────────────────────────────────────
_THU_MUC_GD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CACHE_TROI_CHAN = []

def _load_troi_chan():
    global _CACHE_TROI_CHAN
    if _CACHE_TROI_CHAN:
        return _CACHE_TROI_CHAN
    thu_muc = os.path.join(_THU_MUC_GD, "tai_nguyen", "skill", "troi_chan")
    if not os.path.isdir(thu_muc):
        return _CACHE_TROI_CHAN
    for i in range(1, 61):
        path = os.path.join(thu_muc, f"{i}.png")
        if not os.path.isfile(path):
            break
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (T, T))
            _CACHE_TROI_CHAN.append(img)
        except Exception:
            pass
    return _CACHE_TROI_CHAN


# ── Fallback surface khi chưa có ảnh ─────────────────────
def _ve_fallback():
    s = pygame.Surface((T, T), pygame.SRCALPHA)
    pygame.draw.rect(s, (180, 80, 20, 200), (4, 4, T-8, T-8), border_radius=6)
    pygame.draw.rect(s, (240, 140, 40, 255), (4, 4, T-8, T-8), 2, border_radius=6)
    # Vẽ dây xích đơn giản
    for y in range(6, T-6, 8):
        pygame.draw.ellipse(s, (220, 160, 60, 220), (T//2-8, y, 16, 6))
    return s


# ══════════════════════════════════════════════════════════
#  HIỆU ỨNG TRÓI CHÂN
# ══════════════════════════════════════════════════════════
class HieuUngTroiChan:
    """
    Sử dụng:
        hieu_ung = HieuUngTroiChan()

        # Kích hoạt
        hieu_ung.bat_dau()

        # Mỗi frame trong update():
        hieu_ung.update(nhan_vat)

        # Mỗi frame trong ve() — vẽ dưới chân nhân vật
        hieu_ung.ve(screen, cam_x, cam_y, nhan_vat)

        # Kiểm tra đang active
        if hieu_ung.dang_hoat_dong: ...
    """

    TONG_GIAY    = 5.0
    XUAT_HIEN    = 2.0   # 0→2s  : 1→60
    DUY_TRI      = 1.0   # 2→3s  : giữ
    BIEN_MAT     = 2.0   # 3→5s  : 60→1
    KHOA_BAT_DAU = 1.0   # giây bắt đầu khóa
    KHOA_KET_THUC= 4.0   # giây kết thúc khóa

    # Tốc độ: 60 ảnh / 2 giây / 60fps = 1 ảnh/2 frame → spd=2
    SPD = 2

    def __init__(self):
        self._active  = False
        self._dem     = 0        # frame đã chạy
        self._frames  = []
        self.image    = None
        self._fallback= None

    @property
    def dang_hoat_dong(self):
        return self._active

    @property
    def dang_khoa(self):
        """True khi player bị khóa (giây 1-4)."""
        if not self._active:
            return False
        giay = self._dem / FPS
        return self.KHOA_BAT_DAU <= giay < self.KHOA_KET_THUC

    def bat_dau(self):
        # ---> THÊM 2 DÒNG NÀY VÀO <---
        # Nếu hiệu ứng đang hoạt động rồi thì bỏ qua, không reset lại từ đầu
        if self._active:
            return

        self._active = True
        self._dem    = 0
        self._frames = _load_troi_chan()
        if not self._fallback:
            self._fallback = _ve_fallback()

    def _lay_anh(self):
        """Tính index ảnh theo thời gian."""
        frames = self._frames
        n = len(frames) if frames else 0
        giay  = self._dem / FPS

        if n == 0:
            # Không có ảnh → dùng fallback chỉ khi đang khóa
            if self.dang_khoa:
                s = self._fallback.copy()
                s.set_alpha(int(200 * min(1.0, (giay - self.KHOA_BAT_DAU) /
                                           self.XUAT_HIEN)))
                return s
            return None

        if giay < self.XUAT_HIEN:
            # 0→2s: 1→60 (index 0→n-1)
            tl  = giay / self.XUAT_HIEN
            idx = min(int(tl * n), n - 1)
        elif giay < self.XUAT_HIEN + self.DUY_TRI:
            # 2→3s: giữ frame cuối
            idx = n - 1
        else:
            # 3→5s: 60→1 (index n-1→0)
            tl  = (giay - self.XUAT_HIEN - self.DUY_TRI) / self.BIEN_MAT
            # --- ĐÃ SỬA: Thêm min(n - 1, ...) để chặn lỗi vỡ index ở giây thứ 3.0 ---
            idx = min(n - 1, max(0, int((1.0 - tl) * n)))

        return frames[idx]

    def update(self, nhan_vat):
        if not self._active:
            return

        self._dem += 1

        # Kết thúc
        if self._dem >= int(self.TONG_GIAY * FPS):
            self._active = False
            self._mo_khoa(nhan_vat)
            self.image = None
            return

        # Tính ảnh hiện tại
        self.image = self._lay_anh()

        # Khóa / mở khóa nhân vật
        if self.dang_khoa:
            self._khoa_nhan_vat(nhan_vat)
        else:
            self._mo_khoa(nhan_vat)

    def _khoa_nhan_vat(self, nv):
        """Khóa di chuyển, giữ nguyên vị trí không khí nếu đang bay."""
        # Tốc độ ngang = 0
        nv.vel_x = 0
        # Giữ nguyên độ cao (không rơi thêm)
        nv.vel_y = 0
        # Tắt dash nếu đang dash
        nv._dash_frames = 0
        # Tắt bay
        nv._bay_active  = False
        # Tắt các signal
        nv._danh_signal = False
        nv._nem_signal  = False
        # Chặn phím (ghi đè xu_ly_phim bằng flag)
        nv._khoa_hieu_ung = True

    def _mo_khoa(self, nv):
        nv._khoa_hieu_ung = False

    def ve(self, screen, cam_x, cam_y, nhan_vat):
        """Vẽ hiệu ứng dưới chân nhân vật (1×1 tile)."""
        if not self._active or self.image is None:
            return
        # Đặt ảnh tại chân nhân vật
        x = nhan_vat.rect.centerx - T//2 - cam_x
        y = nhan_vat.rect.bottom  - T    - cam_y
        screen.blit(self.image, (x, y))


# ══════════════════════════════════════════════════════════
#  HIỆU ỨNG ĐÓNG BĂNG
# ══════════════════════════════════════════════════════════
_CACHE_DONG_BANG = []   # 4 ảnh, mỗi ảnh 2×2 tile

def _load_dong_bang():
    global _CACHE_DONG_BANG
    if _CACHE_DONG_BANG:
        return _CACHE_DONG_BANG
    thu_muc = os.path.join(_THU_MUC_GD, "tai_nguyen", "skill", "dong_bang")
    if not os.path.isdir(thu_muc):
        return _CACHE_DONG_BANG
    for i in range(1, 5):
        path = os.path.join(thu_muc, f"{i}.png")
        if not os.path.isfile(path):
            break
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (T * 2, T * 2))
            _CACHE_DONG_BANG.append(img)
        except Exception:
            pass
    return _CACHE_DONG_BANG


def _ve_fallback_dong_bang(cap):
    """Fallback 2×2 tile khi chưa có ảnh, màu xanh băng đậm dần theo cấp."""
    W = T * 2
    s = pygame.Surface((W, W), pygame.SRCALPHA)
    alpha = 80 + cap * 45          # cấp 0→3: 80, 125, 170, 215
    mau   = (60, 180, 240, alpha)
    vien  = (140, 220, 255, 255)
    pygame.draw.rect(s, mau,  (2, 2, W-4, W-4), border_radius=10)
    pygame.draw.rect(s, vien, (2, 2, W-4, W-4), 2, border_radius=10)
    # Vẽ tinh thể băng đơn giản
    cx, cy = W // 2, W // 2
    for ang in range(0, 360, 60):
        import math
        rad = math.radians(ang)
        ex  = cx + int((W // 2 - 8) * math.cos(rad))
        ey  = cy + int((W // 2 - 8) * math.sin(rad))
        pygame.draw.line(s, vien, (cx, cy), (ex, ey), 2)
    return s


class HieuUngDongBang:
    """
    Đóng băng nhân vật vĩnh viễn cho đến khi đánh thường F đủ 4 lần.
    - Hiển thị ảnh 2×2 tile đặt trung tâm vào nhân vật.
    - Cấp băng: 0 → ảnh 1, 1 → ảnh 2, 2 → ảnh 3, 3 → ảnh 4.
    - Mỗi lần F đánh trúng (nhan_vat._danh_signal == True) → cap tăng 1.
    - Cap = 4 → kết thúc hiệu ứng.
    - Cấm: di chuyển, nhảy, dash, bay, ném.
    - Cho phép: F đánh thường, Q.

    Sử dụng:
        # Kích hoạt
        self.hieu_ung.kich_hoat('dong_bang')

        # Thông báo player vừa đánh F (gọi trong update của ManChoi)
        self.hieu_ung.dong_bang.nhan_danh(nhan_vat)

        # Kiểm tra đang bị đóng băng
        if self.hieu_ung.dang_bi_dong_bang: ...
    """

    SO_LAN_PHA = 4   # số lần đánh để phá băng

    def __init__(self):
        self._active  = False
        self._cap     = 0          # 0-3: ảnh hiện tại (index)
        self._frames  = []
        self._fallbacks = []
        self.image    = None

    @property
    def dang_hoat_dong(self):
        return self._active

    def bat_dau(self):
        """Kích hoạt đóng băng. Nếu đang active thì bỏ qua."""
        if self._active:
            return
        self._active = True
        self._cap    = 0
        self._frames = _load_dong_bang()
        if not self._fallbacks:
            self._fallbacks = [_ve_fallback_dong_bang(c) for c in range(4)]
        self.image = self._lay_anh()

    def nhan_danh(self, nhan_vat=None):
        """Gọi mỗi khi player đánh F thành công khi đang bị đóng băng."""
        if not self._active:
            return
        self._cap += 1
        if self._cap >= self.SO_LAN_PHA:
            self._active = False
            self.image   = None
            if nhan_vat is not None:
                nhan_vat._khoa_dong_bang = False
        else:
            self.image = self._lay_anh()

    def _lay_anh(self):
        """Trả về surface ứng với cấp băng hiện tại."""
        idx = min(self._cap, self.SO_LAN_PHA - 1)
        if self._frames and idx < len(self._frames):
            return self._frames[idx]
        # Fallback
        if self._fallbacks and idx < len(self._fallbacks):
            return self._fallbacks[idx]
        return None

    def update(self, nhan_vat):
        if not self._active:
            return

        # Khóa di chuyển nhưng cho phép F và Q
        nhan_vat.vel_x        = 0
        nhan_vat.vel_y        = 0
        nhan_vat._dash_frames = 0
        nhan_vat._bay_active  = False
        nhan_vat._nem_signal  = False
        # KHÔNG khóa _danh_signal — để F đánh phá băng được
        # KHÔNG set _khoa_hieu_ung — để Q vẫn dùng được
        # Dùng flag riêng để nhan_vat biết đang bị băng
        nhan_vat._khoa_dong_bang = True

    def ket_thuc(self, nhan_vat):
        """Mở khóa khi băng tan."""
        nhan_vat._khoa_dong_bang = False

    def ve(self, screen, cam_x, cam_y, nhan_vat):
        """Vẽ 2×2 tile đặt trung tâm vào nhân vật."""
        if not self._active or self.image is None:
            return
        W = T * 2
        x = nhan_vat.rect.centerx - W // 2 - cam_x
        y = nhan_vat.rect.centery - W // 2 - cam_y
        screen.blit(self.image, (x, y))


# ══════════════════════════════════════════════════════════
#  HIỆU ỨNG BẤT TỬ
# ══════════════════════════════════════════════════════════
_CACHE_BAT_TU = None   # 1 ảnh duy nhất

def _load_bat_tu():
    global _CACHE_BAT_TU
    if _CACHE_BAT_TU is not None:
        return _CACHE_BAT_TU
    path = os.path.join(_THU_MUC_GD, "tai_nguyen", "skill", "battu.png")
    if os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            # Scale vừa khít nhân vật (1×2 tile)
            img = pygame.transform.scale(img, (T*2, T * 2))
            _CACHE_BAT_TU = img
        except Exception:
            pass
    if _CACHE_BAT_TU is None:
        # Fallback: vòng tròn vàng sáng
        s = pygame.Surface((T, T * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(s, (255, 220, 50, 160), (2, 2, T-4, T*2-4))
        pygame.draw.ellipse(s, (255, 255, 150, 220), (2, 2, T-4, T*2-4), 3)
        _CACHE_BAT_TU = s
    return _CACHE_BAT_TU


class HieuUngBatTu:
    """
    Bất tử 3 giây — nhân vật không mất máu.
    - Hiển thị ảnh battu.png đặt trùng nhân vật.
    - 1 giây cuối: nhấp nháy (xen kẽ hiện/ẩn mỗi 6 frame).
    - Không khóa bất kỳ hành động nào.

    Sử dụng:
        self.hieu_ung.kich_hoat('bat_tu')
        if self.hieu_ung.dang_bat_tu: ...   # kiểm tra bất tử
    """

    TONG_GIAY    = 3              # tổng thời gian (giây)
    TONG_FRAME   = TONG_GIAY * FPS
    NHAP_NHAY_TU = 2 * FPS        # bắt đầu nhấp nháy từ giây 2 (1 giây cuối)
    NHAP_NHAY_CK = 6              # chu kỳ nhấp nháy: 6 frame/lần

    def __init__(self):
        self._active = False
        self._dem    = 0
        self._anh    = None
        self.image   = None        # surface hiện tại (None = ẩn)

    @property
    def dang_hoat_dong(self):
        return self._active

    def bat_dau(self):
        """Kích hoạt bất tử. Nếu đang active thì reset lại timer."""
        self._active = True
        self._dem    = 0
        self._anh    = _load_bat_tu()
        self.image   = self._anh

    def update(self, nhan_vat):
        if not self._active:
            return

        self._dem += 1

        # Kết thúc
        if self._dem >= self.TONG_FRAME:
            self._active = False
            self.image   = None
            return

        # 1 giây cuối: nhấp nháy
        con_lai = self.TONG_FRAME - self._dem
        if con_lai <= FPS:
            # Xen kẽ hiện/ẩn theo chu kỳ NHAP_NHAY_CK
            hien = (self._dem // self.NHAP_NHAY_CK) % 2 == 0
            self.image = self._anh if hien else None
        else:
            self.image = self._anh

    def ve(self, screen, cam_x, cam_y, nhan_vat):
        """Vẽ ảnh trùng với vị trí nhân vật."""
        if not self._active or self.image is None:
            return
        x = nhan_vat.rect.x - cam_x
        y = nhan_vat.rect.y - cam_y
        screen.blit(self.image, (x, y))


# ══════════════════════════════════════════════════════════
#  HIỆU ỨNG TẤN CÔNG F — vệt chém 2×2 tile
# ══════════════════════════════════════════════════════════
_CACHE_TAN_CONG = None   # ảnh tancong.png gốc (chưa flip)
_CACHE_KIEM_CAM = None   # ảnh kiem.png (cầm tay, 1×2 tile)

def _load_tan_cong():
    global _CACHE_TAN_CONG
    if _CACHE_TAN_CONG is not None:
        return _CACHE_TAN_CONG
    path = os.path.join(_THU_MUC_GD, "tai_nguyen", "hinh_anh", "nhan_vat", "tancong.png")
    if os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (T*2, T*2))
            _CACHE_TAN_CONG = img
            return img
        except Exception:
            pass
    s = pygame.Surface((T*2, T*2), pygame.SRCALPHA)
    pygame.draw.line(s, (255,255,255,220), (T*2-6, 6), (6, T*2-6), 8)
    _CACHE_TAN_CONG = s
    return s

def _load_kiem_cam():
    """Load kiem.png 1×2 tile để vẽ kiếm trên tay nhân vật."""
    global _CACHE_KIEM_CAM
    if _CACHE_KIEM_CAM is not None:
        return _CACHE_KIEM_CAM
    path = os.path.join(_THU_MUC_GD, "tai_nguyen", "hinh_anh", "nhan_vat", "kiem.png")
    if os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            # Scale 1×2 tile theo tỉ lệ ảnh gốc: giữ width=T, tính height
            ow, oh = img.get_size()
            # ảnh kiếm dọc: width=T//2, height=T*2 (mỏng dọc)
            img = pygame.transform.scale(img, (T // 2, T * 2))
            _CACHE_KIEM_CAM = img
            return img
        except Exception:
            pass
    # Fallback
    s = pygame.Surface((T//2, T*2), pygame.SRCALPHA)
    pygame.draw.rect(s, (200, 200, 220), (s.get_width()//2-3, 0, 6, T*2), border_radius=2)
    _CACHE_KIEM_CAM = s
    return s


class HieuUngTanCong:
    """
    Hiệu ứng tấn công F — 2 giai đoạn:
      Giai đoạn 1 (0.05s = 3 frame): hiện kiếm giơ lên, ẩn tancong, khóa di chuyển.
      Giai đoạn 2 (0.25s = 15 frame): ẩn kiếm, hiện vệt chém tancong.png.
    Sau khi kết thúc: kiếm hiện lại bình thường (do KiemCamTay xử lý riêng).
    """
    FRAME_GIAI_DOAN_1 = 3    # 0.05s
    FRAME_GIAI_DOAN_2 = 15   # 0.25s
    TONG_FRAME = FRAME_GIAI_DOAN_1 + FRAME_GIAI_DOAN_2  # 18

    def __init__(self):
        self._active    = False
        self._dem       = 0
        self._huong     = 1
        self._anh       = None
        self._anh_flip  = None
        self._kiem      = None
        self._kiem_flip = None
        self.image      = None   # surface vệt chém (None = ẩn)
        self.rect       = None
        # Trạng thái để vẽ kiếm giơ
        self.dang_gd1   = False  # True trong giai đoạn 1 (hiện kiếm giơ)
        # Để KiemCamTay biết đang đánh và ẩn kiếm thường
        self.dang_danh  = False

    @property
    def can_khoa_di_chuyen(self):
        """True trong giai đoạn 1 — khóa di chuyển nhân vật."""
        return self._active and self._dem < self.FRAME_GIAI_DOAN_1

    def kich_hoat(self, player_rect, huong):
        if self._anh is None:
            self._anh      = _load_tan_cong()
            self._anh_flip = pygame.transform.flip(self._anh, True, False)
        if self._kiem is None:
            k = _load_kiem_cam()
            self._kiem      = k
            self._kiem_flip = pygame.transform.flip(k, True, False)

        self._active   = True
        self._dem      = 0
        self._huong    = huong
        self.dang_danh = True
        self.dang_gd1  = True
        self.image     = None
        self.rect      = None
        self._player_rect = player_rect.copy()

    def update(self, nhan_vat=None):
        if not self._active:
            self.dang_danh = False
            self.dang_gd1  = False
            return

        self._dem += 1

        # Cập nhật vị trí theo nhân vật nếu có
        if nhan_vat is not None:
            self._player_rect = nhan_vat.rect.copy()

        # Giai đoạn 1: hiện kiếm giơ, ẩn vệt chém, khóa di chuyển
        if self._dem <= self.FRAME_GIAI_DOAN_1:
            self.dang_gd1  = True
            self.image     = None
            self.rect      = None
            # Khóa di chuyển (không vel_x, không dash)
            if nhan_vat is not None:
                nhan_vat.vel_x        = 0
                nhan_vat._dash_frames = 0

        # Giai đoạn 2: ẩn kiếm giơ, hiện vệt chém tancong
        else:
            self.dang_gd1 = False
            anh = self._anh if self._huong == 1 else self._anh_flip
            self.image = anh
            pr = self._player_rect
            if self._huong == 1:
                self.rect = anh.get_rect(midleft=(pr.centerx - T, pr.centery))
            else:
                self.rect = anh.get_rect(midright=(pr.centerx + T, pr.centery))

        # Hết tổng thời gian
        if self._dem >= self.TONG_FRAME:
            self._active   = False
            self.dang_danh = False
            self.dang_gd1  = False
            self.image     = None
            self.rect      = None

    def ve_giai_doan_1(self, screen, cam_x, cam_y):
        """Vẽ kiếm giơ lên trong giai đoạn 1 — gọi từ man_choi.ve() sau nhân vật."""
        if not self.dang_gd1 or self._kiem is None:
            return
        pr = self._player_rect
        anh = self._kiem if self._huong == 1 else self._kiem_flip
        # Đặt chuôi kiếm ở ngang thắt lưng, lưỡi chỉ lên trên
        # Tay phải: nếu nhìn phải → bên phải nhân vật; nhìn trái → bên trái
        if self._huong == 1:
            x = pr.right - T // 4 - cam_x
        else:
            x = pr.left - T // 4 - cam_x
        y = pr.centery - T - cam_y   # giữa chiều cao, lưỡi lên trên
        screen.blit(anh, (x, y))

    def ve(self, screen, cam_x, cam_y):
        """Vẽ vệt chém tancong trong giai đoạn 2."""
        if not self._active or self.image is None or self.rect is None:
            return
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y - cam_y))


# ══════════════════════════════════════════════════════════
#  QUẢN LÝ NHIỀU HIỆU ỨNG
# ══════════════════════════════════════════════════════════
class QuanLyHieuUng:
    """
    Giữ tất cả hiệu ứng đang active.
    Sử dụng trong ManChoi:
        self.hieu_ung = QuanLyHieuUng()

        # Kích hoạt
        self.hieu_ung.kich_hoat('troi_chan')
        self.hieu_ung.kich_hoat('dong_bang')
        self.hieu_ung.kich_hoat('bat_tu')

        # Thông báo player đánh F (chỉ khi đang bị đóng băng)
        if self.hieu_ung.dang_bi_dong_bang:
            self.hieu_ung.dong_bang.nhan_danh(self.nhan_vat)

        # Kiểm tra bất tử (thay thế _giap_active ở man_choi)
        if self.hieu_ung.dang_bat_tu: ...

        # Mỗi frame
        self.hieu_ung.update(self.nhan_vat)
        self.hieu_ung.ve(screen, cam_x, cam_y, self.nhan_vat)
    """

    def __init__(self):
        self.troi_chan = HieuUngTroiChan()
        self.dong_bang = HieuUngDongBang()
        self.bat_tu    = HieuUngBatTu()
        self.tan_cong  = HieuUngTanCong()

    def kich_hoat(self, ten):
        if ten == 'troi_chan':
            self.troi_chan.bat_dau()
        elif ten == 'dong_bang':
            self.dong_bang.bat_dau()
        elif ten == 'bat_tu':
            self.bat_tu.bat_dau()

    @property
    def dang_bi_troi(self):
        return self.troi_chan.dang_khoa

    @property
    def dang_bi_dong_bang(self):
        return self.dong_bang.dang_hoat_dong

    @property
    def dang_bat_tu(self):
        return self.bat_tu.dang_hoat_dong

    def update(self, nhan_vat):
        self.troi_chan.update(nhan_vat)
        if self.dong_bang.dang_hoat_dong:
            self.dong_bang.update(nhan_vat)
        else:
            if hasattr(nhan_vat, '_khoa_dong_bang') and nhan_vat._khoa_dong_bang:
                self.dong_bang.ket_thuc(nhan_vat)
        self.bat_tu.update(nhan_vat)
        self.tan_cong.update(nhan_vat)

    def ve(self, screen, cam_x, cam_y, nhan_vat):
        self.troi_chan.ve(screen, cam_x, cam_y, nhan_vat)
        self.dong_bang.ve(screen, cam_x, cam_y, nhan_vat)
        self.bat_tu.ve(screen, cam_x, cam_y, nhan_vat)
        self.tan_cong.ve_giai_doan_1(screen, cam_x, cam_y)
        self.tan_cong.ve(screen, cam_x, cam_y)
