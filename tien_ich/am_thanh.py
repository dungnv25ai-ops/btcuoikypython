# ============================================================
#  tien_ich/am_thanh.py — Quản lý nhạc nền + sfx
# ============================================================

import os
import pygame

# ── Đường dẫn thư mục âm thanh ───────────────────────────
_THU_MUC = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),   # my_game/
    "tai_nguyen", "am_thanh"
)

# ── Mapping key → tên file (không kèm đuôi) ─────────────
# Đã xóa 1 key man_1_4 bị lặp và đảm bảo mọi file trỏ đúng tên
_NHAC_NEN = {
    "menu"       : "nen",
    "man_1_4"    : "nhac",
    "man_6_9"    : "nhac",
    "boss_5"     : "nhac",
    "boss_10_p1" : "nhac",
    "boss_10_p2" : "nhac",
}

# Đã bỏ đuôi .mov đi vì Pygame không hỗ trợ. Nó sẽ tự lấy file .mp3
_DUOI_UU_TIEN = [".mp3", ".ogg", ".wav"]


def _tim_file(ten_goc):
    """Tìm file âm thanh theo tên gốc, thử các đuôi ưu tiên."""
    for duoi in _DUOI_UU_TIEN:
        path = os.path.join(_THU_MUC, ten_goc + duoi)
        if os.path.isfile(path):
            return path
    return None


class AmThanh:
    """Quản lý toàn bộ âm thanh game — tạo 1 instance duy nhất."""

    def __init__(self, am_luong_nhac=0.7, am_luong_sfx=1.0):
        # Đảm bảo mixer đã init
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        self._nhac_hien_tai = None   # key đang phát
        self._am_luong_nhac = am_luong_nhac
        self._am_luong_sfx  = am_luong_sfx
        self._sfx_click     = self._tai_sfx("click")
        self._tat           = False  # True = tắt hết âm thanh

    # ── Nội bộ ───────────────────────────────────────────
    def _tai_sfx(self, ten):
        path = _tim_file(ten)
        if path:
            try:
                return pygame.mixer.Sound(path)
            except Exception:
                pass
        return None

    # ── API công khai ─────────────────────────────────────
    def choi_nhac(self, key: str):
        """Phát nhạc nền theo key. Không làm gì nếu đang phát cùng key."""
        if self._tat:
            return
        if key == self._nhac_hien_tai:
            return   # đang phát rồi, không restart

        ten = _NHAC_NEN.get(key)
        if ten is None:
            return

        path = _tim_file(ten)
        if path is None:
            # Không có file → dừng nhạc cũ, không báo lỗi
            pygame.mixer.music.stop()
            self._nhac_hien_tai = None
            return

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self._am_luong_nhac)
            pygame.mixer.music.play(-1)   # loop vô hạn
            self._nhac_hien_tai = key
        except Exception:
            self._nhac_hien_tai = None

    def phat_click(self):
        """Phát sfx click menu."""
        if self._tat or self._sfx_click is None:
            return
        try:
            self._sfx_click.set_volume(self._am_luong_sfx)
            self._sfx_click.play()
        except Exception:
            pass

    def dung(self):
        """Dừng nhạc nền."""
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        self._nhac_hien_tai = None

    def tam_dung(self):
        """Tạm dừng (pause menu)."""
        try:
            pygame.mixer.music.pause()
        except Exception:
            pass

    def tiep_tuc(self):
        """Tiếp tục sau khi tạm dừng."""
        if self._tat:
            return
        try:
            pygame.mixer.music.unpause()
        except Exception:
            pass

    def tang_am(self, muc: float):
        """Chỉnh âm lượng nhạc nền (0.0 – 1.0)."""
        self._am_luong_nhac = max(0.0, min(1.0, muc))
        try:
            pygame.mixer.music.set_volume(self._am_luong_nhac)
        except Exception:
            pass

    def tang_am_sfx(self, muc: float):
        """Chỉnh âm lượng sfx (0.0 – 1.0)."""
        self._am_luong_sfx = max(0.0, min(1.0, muc))

    def tat_am(self, tat: bool):
        """True = tắt hết âm thanh."""
        self._tat = tat
        if tat:
            self.dung()

    @property
    def dang_phat(self):
        return self._nhac_hien_tai