# ============================================================
#  man_hinh/thong_tin.py — Thông tin trò chơi
# ============================================================

import pygame
from cai_dat import *

NOI_DUNG = [
    ("Tên trò chơi",  TEN_GAME),
    ("Thể loại",      "LOST IN TIME - Quá Khử Lãng Quên"),
    ("Công cụ",       "Python 3 + Pygame"),
    ("Số màn chơi",   "10 man  (Boss o man 5 va 10)"),
    ("Phiên bản",     "v0.1  Prototype"),
    ("Lập trình",     "Sinh vien nam 1"),
]


class ThongTin:
    def __init__(self, man_hinh):
        self.man_hinh = man_hinh

    def _tao_font(self):
        w, h = self.man_hinh.get_size()
        self.font_tieude = pygame.font.SysFont(FONT_CHINH, max(24, h // 14), bold=True)
        self.font_nhan   = pygame.font.SysFont(FONT_CHINH, max(14, h // 26), bold=True)
        self.font_gia_tri= pygame.font.SysFont(FONT_CHINH, max(14, h // 26))

    def update(self):
        self._tao_font()

    def ve(self):
        w, h = self.man_hinh.get_size()
        self._tao_font()
        self.man_hinh.fill((18, 18, 40))

        # Tiêu đề
        tieu = self.font_tieude.render("Thong Tin Tro Choi", True, VANG)
        ty = h // 10
        self.man_hinh.blit(tieu, tieu.get_rect(center=(w//2, ty)))
        pygame.draw.line(self.man_hinh, (60, 60, 120),
                         (w//2 - 200, ty + 22), (w//2 + 200, ty + 22), 1)

        # Bảng thông tin — tự căn theo h
        so_dong   = len(NOI_DUNG)
        vung_cao  = h * 0.68
        dong_cao  = vung_cao / so_dong
        bat_dau_y = h * 0.22
        le_x      = w * 0.1
        cot2_x    = w * 0.45

        for i, (nhan, gia_tri) in enumerate(NOI_DUNG):
            y = int(bat_dau_y + i * dong_cao)
            r = pygame.Rect(int(le_x - 8), y - 4, int(w * 0.8), int(dong_cao - 6))

            mau_nen = (30, 30, 65) if i % 2 == 0 else (22, 22, 50)
            pygame.draw.rect(self.man_hinh, mau_nen, r, border_radius=8)

            t_n = self.font_nhan.render(nhan, True, CAM)
            t_g = self.font_gia_tri.render(gia_tri, True, TRANG)
            cy  = y + int(dong_cao // 2) - t_n.get_height() // 2
            self.man_hinh.blit(t_n, (int(le_x), cy))
            self.man_hinh.blit(t_g, (int(cot2_x), cy))

        # ESC
        font_esc = self.font_gia_tri
        esc = font_esc.render("ESC: Quay lai menu", True, (70, 70, 110))
        self.man_hinh.blit(esc, esc.get_rect(center=(w//2, h - int(h * 0.05))))

    def xu_ly_su_kien(self, su_kien):
        if su_kien.type == pygame.KEYDOWN and su_kien.key == pygame.K_ESCAPE:
            return TRANG_THAI_MENU
        if su_kien.type == pygame.MOUSEBUTTONDOWN:
            return TRANG_THAI_MENU
        return TRANG_THAI_THONG_TIN
