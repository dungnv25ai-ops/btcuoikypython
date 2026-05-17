# ============================================================
#  man_hinh/huong_dan.py — Hướng dẫn chơi
# ============================================================

import pygame
from cai_dat import *

CAC_MUC_HUONG_DAN = [
    ("DI CHUYỂN",  [
        ("← →  hoặc  A D",  "Chạy sang trái / phải"),
        ("Space / W / ↑",   "Nhảy lên"),
    ]),
    ("MỤC TIÊU", [
        ("★  Ô vàng",       "Đứng vào đây để qua màn"),
        ("H  Hộp gỗ",       "Đẩy hộp vào đúng vị trí"),
    ]),
    ("PHÍM HỆ THỐNG", [
        ("ESC",             "Quay lại menu"),
        ("R",               "Chơi lại màn hiện tại"),
        ("F11",             "Bật / tắt toàn màn hình"),
    ]),
    ("MÀN ĐẶC BIỆT", [
        ("Màn 5",           "Boss trung gian — khó hơn bình thường"),
        ("Màn 10",          "Boss cuối — thử thách cao nhất!"),
    ]),
]


class HuongDan:
    def __init__(self, man_hinh):
        self.man_hinh = man_hinh
        self._tao_font()

    def _tao_font(self):
        w, h = self.man_hinh.get_size()
        self.font_tieude  = pygame.font.SysFont(FONT_CHINH, max(26, h // 14), bold=True)
        self.font_nhom    = pygame.font.SysFont(FONT_CHINH, max(14, h // 28), bold=True)
        self.font_noi_dung= pygame.font.SysFont(FONT_CHINH, max(13, h // 32))
        self.font_phim    = pygame.font.SysFont(FONT_CHINH, max(12, h // 40))

    def update(self):
        self._tao_font()

    def ve(self):
        w, h = self.man_hinh.get_size()
        self.man_hinh.fill((18, 18, 40))

        # Tiêu đề
        tieu = self.font_tieude.render("📖  Hướng Dẫn Chơi", True, VANG)
        self.man_hinh.blit(tieu, tieu.get_rect(center=(w//2, h // 12)))
        pygame.draw.line(self.man_hinh, (60, 60, 120),
                         (w//2 - 220, h//12 + 22), (w//2 + 220, h//12 + 22), 1)

        # Chia 2 cột
        cot_x = [w // 8, w // 2 + 20]
        y_bat_dau = h // 7

        muc_idx = 0
        for cot in range(2):
            y = y_bat_dau
            for _ in range(2):  # 2 nhóm mỗi cột
                if muc_idx >= len(CAC_MUC_HUONG_DAN):
                    break
                nhom, ds = CAC_MUC_HUONG_DAN[muc_idx]
                muc_idx += 1

                # Tên nhóm
                t_nhom = self.font_nhom.render(nhom, True, CAM)
                self.man_hinh.blit(t_nhom, (cot_x[cot], y))
                y += t_nhom.get_height() + 4
                pygame.draw.line(self.man_hinh, (60, 60, 100),
                                 (cot_x[cot], y), (cot_x[cot] + w//2 - 40, y), 1)
                y += 8

                for phim, mo_ta in ds:
                    # Nền dòng
                    r = pygame.Rect(cot_x[cot] - 8, y - 3, w//2 - 30, 26)
                    pygame.draw.rect(self.man_hinh, (30, 30, 65), r, border_radius=6)

                    t_phim = self.font_noi_dung.render(phim, True, VANG)
                    t_mo   = self.font_noi_dung.render(mo_ta, True, (200, 200, 200))
                    self.man_hinh.blit(t_phim, (cot_x[cot], y))
                    self.man_hinh.blit(t_mo,   (cot_x[cot] + 160, y))
                    y += 32

                y += 20  # khoảng cách giữa nhóm

        # Phím thoát
        hdl = self.font_phim.render("ESC: Quay lại menu", True, (90, 90, 130))
        self.man_hinh.blit(hdl, hdl.get_rect(center=(w//2, h - 18)))

    def xu_ly_su_kien(self, su_kien):
        if su_kien.type == pygame.KEYDOWN:
            if su_kien.key == pygame.K_ESCAPE:
                return TRANG_THAI_MENU
        if su_kien.type == pygame.MOUSEBUTTONDOWN:
            return TRANG_THAI_MENU
        return TRANG_THAI_HUONG_DAN
