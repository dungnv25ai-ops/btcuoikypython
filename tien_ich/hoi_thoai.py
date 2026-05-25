# ============================================================
#  tien_ich/hoi_thoai.py — Hệ thống hội thoại 2 loại
#
#  Loại 1 — HoiThoai (hộp đen dưới màn):
#    Kích hoạt khi bắt đầu màn, Enter để next/đóng.
#
#  Loại 2 — ThongBao (nổi giữa màn):
#    Kích hoạt khi nhặt vật phẩm, Enter để đóng.
#
#  Khi đang hiển thị → trả về dang_hien=True
#  Man_choi dùng flag này để tạm dừng mọi thứ.
# ============================================================

import pygame
import math
from cai_dat import *


# ── Loại 1: Hội thoại nhiều dòng (hộp đen dưới) ─────────
class HoiThoai:
    """
    Dùng trong _tai_ban_do:
        self.hoi_thoai.bat_dau([
            ("Tên", "Nội dung dòng 1"),
            ("Tên", "Nội dung dòng 2"),
        ])

    Trong xu_ly_su_kien:
        if self.hoi_thoai.dang_hien:
            self.hoi_thoai.xu_ly(su_kien)
            return TRANG_THAI_CHOI

    Trong update — BỎ QUA mọi update khi dang_hien=True.
    Trong ve — gọi cuối cùng: self.hoi_thoai.ve(screen)
    """

    HANG_CAO   = 160    # chiều cao hộp thoại
    TOC_DO_CHU = 1      # số ký tự hiện mỗi frame (typewriter)

    def __init__(self):
        self.dang_hien = False
        self._cac_dong = []   # list (ten, noi_dung)
        self._index    = 0    # dòng hiện tại
        self._hien_n   = 0    # số ký tự đang hiển thị
        self._xong_dong= False
        self._font_ten = self._font_chu = None

    def bat_dau(self, cac_dong):
        """cac_dong = [(ten, noi_dung), ...] hoặc [(noi_dung,), ...]"""
        if not cac_dong:
            return
        # Chuẩn hoá: nếu là str thì wrap thành ("", str)
        self._cac_dong = []
        for d in cac_dong:
            if isinstance(d, str):
                self._cac_dong.append(("", d))
            elif len(d) == 1:
                self._cac_dong.append(("", d[0]))
            else:
                self._cac_dong.append((d[0], d[1]))
        self._index     = 0
        self._hien_n    = 0
        self._xong_dong = False
        self.dang_hien  = True

    def xu_ly(self, su_kien):
        """Gọi khi dang_hien=True. Trả về True nếu vẫn đang hiện."""
        if not self.dang_hien:
            return False
        if su_kien.type == pygame.KEYDOWN and su_kien.key in (
                pygame.K_RETURN, pygame.K_SPACE, pygame.K_z):
            if not self._xong_dong:
                # Hiện hết cả dòng ngay
                noi_dung = self._cac_dong[self._index][1]
                self._hien_n  = len(noi_dung)
                self._xong_dong = True
            else:
                # Chuyển dòng tiếp hoặc đóng
                self._index += 1
                if self._index >= len(self._cac_dong):
                    self.dang_hien = False
                else:
                    self._hien_n    = 0
                    self._xong_dong = False
        return self.dang_hien

    def update(self):
        """Gọi mỗi frame để typewriter effect."""
        if not self.dang_hien:
            return
        noi_dung = self._cac_dong[self._index][1]
        if self._hien_n < len(noi_dung):
            self._hien_n = min(self._hien_n + self.TOC_DO_CHU, len(noi_dung))
        else:
            self._xong_dong = True

    def ve(self, screen):
        if not self.dang_hien:
            return
        w, h = screen.get_size()
        if not self._font_ten:
            self._font_ten = pygame.font.SysFont(FONT_CHINH, 15, bold=True)
            self._font_chu = pygame.font.SysFont(FONT_CHINH, 16)

        ten, noi_dung = self._cac_dong[self._index]

        # Hộp đen
        bx, by = 0, h - self.HANG_CAO
        pygame.draw.rect(screen, (5, 5, 15),
                         (bx, by, w, self.HANG_CAO))
        pygame.draw.rect(screen, (80, 80, 140),
                         (bx, by, w, self.HANG_CAO), 2)
        pygame.draw.line(screen, (80, 80, 140), (bx, by), (bx+w, by), 2)

        # Tên nhân vật
        PAD = 16
        if ten:
            t_ten = self._font_ten.render(ten, True, VANG)
            screen.blit(t_ten, (PAD, by + PAD - 2))
            text_y = by + PAD + t_ten.get_height() + 4
        else:
            text_y = by + PAD + 4

        # Nội dung (typewriter, tự xuống dòng)
        hien = noi_dung[:self._hien_n]
        cac_dong = self._ngat_dong(hien, w - PAD*2)
        for dong in cac_dong:
            t = self._font_chu.render(dong, True, TRANG)
            screen.blit(t, (PAD, text_y))
            text_y += t.get_height() + 4

        # Gợi ý Enter
        if self._xong_dong:
            a = int(180 + 75*abs(math.sin(pygame.time.get_ticks()*0.004)))
            ky = "▶ Tiếp" if self._index < len(self._cac_dong)-1 else "▶ Đóng"
            t_hint = self._font_ten.render(ky, True, (180, 180, 220))
            t_hint.set_alpha(a)
            screen.blit(t_hint, (w - t_hint.get_width() - PAD,
                                  h - t_hint.get_height() - 8))

    def _ngat_dong(self, text, max_w):
        if not self._font_chu:
            return [text]
        tu, dong, hien = text.split(), [], ""
        for t in tu:
            tmp = (hien + " " + t).strip()
            if self._font_chu.size(tmp)[0] <= max_w:
                hien = tmp
            else:
                if hien: dong.append(hien)
                hien = t
        if hien: dong.append(hien)
        return dong or [""]


# ── Loại 2: Thông báo nổi giữa màn ──────────────────────
class ThongBao:
    """
    Dùng khi nhặt vật phẩm:
        self.thong_bao.hien("Bạn đã nhặt được Kiếm!")

    Trong xu_ly_su_kien:
        if self.thong_bao.dang_hien:
            self.thong_bao.xu_ly(su_kien)
            return TRANG_THAI_CHOI

    Trong ve — gọi cuối: self.thong_bao.ve(screen)
    """

    def __init__(self):
        self.dang_hien = False
        self._tieu_de  = ""
        self._noi_dung = ""
        self._font_tieu= self._font_chu = None
        self._dem      = 0

    def hien(self, noi_dung, tieu_de="Thông báo"):
        self.dang_hien = True
        self._tieu_de  = tieu_de
        self._noi_dung = noi_dung
        self._dem      = 0

    def xu_ly(self, su_kien):
        if not self.dang_hien:
            return False
        if su_kien.type == pygame.KEYDOWN and su_kien.key in (
                pygame.K_RETURN, pygame.K_SPACE, pygame.K_z,
                pygame.K_ESCAPE):
            self.dang_hien = False
        return self.dang_hien

    def update(self):
        if self.dang_hien:
            self._dem += 1

    def ve(self, screen):
        if not self.dang_hien:
            return
        w, h = screen.get_size()
        if not self._font_tieu:
            self._font_tieu = pygame.font.SysFont(FONT_CHINH, 18, bold=True)
            self._font_chu  = pygame.font.SysFont(FONT_CHINH, 15)

        BW = min(420, w-80); PAD = 20
        # Tính chiều cao
        dong = self._wrap(self._noi_dung, BW-PAD*2)
        BH = PAD*2 + 30 + len(dong)*22 + 30
        bx = w//2 - BW//2; by = h//2 - BH//2

        # Overlay
        ov = pygame.Surface((w, h), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 140))
        screen.blit(ov, (0, 0))

        # Hộp
        pygame.draw.rect(screen, (10, 10, 30), (bx, by, BW, BH), border_radius=12)
        pygame.draw.rect(screen, VANG, (bx, by, BW, BH), 2, border_radius=12)

        # Tiêu đề
        t_tieu = self._font_tieu.render(self._tieu_de, True, VANG)
        screen.blit(t_tieu, t_tieu.get_rect(center=(w//2, by+PAD+8)))
        pygame.draw.line(screen, (80, 80, 120),
                         (bx+PAD, by+PAD+28), (bx+BW-PAD, by+PAD+28), 1)

        # Nội dung
        ty = by + PAD + 36
        for d in dong:
            t = self._font_chu.render(d, True, TRANG)
            screen.blit(t, t.get_rect(center=(w//2, ty)))
            ty += 22

        # Gợi ý
        a = int(180 + 75*abs(math.sin(self._dem*0.05)))
        t_hint = self._font_chu.render("[ Enter ] Đóng", True, (160, 160, 200))
        t_hint.set_alpha(a)
        screen.blit(t_hint, t_hint.get_rect(center=(w//2, by+BH-16)))

    def _wrap(self, text, max_w):
        if not self._font_chu:
            return [text]
        tu, dong, hien = text.split(), [], ""
        for t in tu:
            tmp = (hien + " " + t).strip()
            if self._font_chu.size(tmp)[0] <= max_w:
                hien = tmp
            else:
                if hien: dong.append(hien)
                hien = t
        if hien: dong.append(hien)
        return dong or [""]
