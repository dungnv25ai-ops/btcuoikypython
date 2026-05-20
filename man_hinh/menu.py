# ============================================================
#  man_hinh/menu.py — Menu chính
#  Hỗ trợ: chuột, bàn phím, fullscreen F11, resize cửa sổ
# ============================================================

import pygame
from cai_dat import *

class Menu:
    def __init__(self, man_hinh):
        self.man_hinh = man_hinh
        self._tao_font()

        self.cac_muc = [
            ("  Chọn màn",           TRANG_THAI_CHON_MAN),
            ("   Trò chơi khác",      TRANG_THAI_TRO_CHOI_KHAC),
            ("   Hướng dẫn",          TRANG_THAI_HUONG_DAN),
            ("   Thông tin trò chơi", TRANG_THAI_THONG_TIN),
        ]
        self.muc_dang_chon = 0
        self.cac_rect_nut  = []   # lưu vị trí nút để bắt click chuột

    def _tao_font(self):
        w, h = self.man_hinh.get_size()
        self.font_tieude = pygame.font.SysFont(FONT_CHINH, max(28, h // 12), bold=True)
        self.font_muc    = pygame.font.SysFont(FONT_CHINH, max(18, h // 20), bold=True)
        self.font_phim   = pygame.font.SysFont(FONT_CHINH, max(13, h // 38))

    def update(self):
        # Tạo lại font khi cửa sổ thay đổi kích thước
        self._tao_font()
        if hasattr(self, 'am_thanh'):
            self.am_thanh.choi_nhac("menu")

    def ve(self):
        w, h = self.man_hinh.get_size()
        self.cac_rect_nut = []

        # Nền tối
        self.man_hinh.fill((18, 18, 40))

        # Tiêu đề
        bong    = self.font_tieude.render(TEN_GAME, True, DEN)
        tieu_de = self.font_tieude.render(TEN_GAME, True, VANG)
        cy = h // 7
        self.man_hinh.blit(bong,    bong.get_rect(center=(w//2+3, cy+3)))
        self.man_hinh.blit(tieu_de, tieu_de.get_rect(center=(w//2, cy)))

        # Đường kẻ dưới tiêu đề
        pygame.draw.line(self.man_hinh, (60, 60, 120),
                         (w//2 - 250, cy + 30), (w//2 + 250, cy + 30), 1)

        # Tính vị trí các nút theo kích thước màn hình
        so_muc    = len(self.cac_muc)
        nut_cao   = max(44, h // 13)
        nut_rong  = min(420, w - 100)
        khoang    = max(10, h // 55)
        tong_cao  = so_muc * nut_cao + (so_muc - 1) * khoang
        bat_dau_y = (h - tong_cao) // 2 + 30

        # Vị trí chuột để hover
        mx, my = pygame.mouse.get_pos()

        for i, (nhan, _) in enumerate(self.cac_muc):
            y   = bat_dau_y + i * (nut_cao + khoang)
            r   = pygame.Rect(w//2 - nut_rong//2, y, nut_rong, nut_cao)
            self.cac_rect_nut.append(r)

            # Hover chuột hoặc đang chọn bằng bàn phím
            hover = r.collidepoint(mx, my)
            chon  = (i == self.muc_dang_chon)

            if chon or hover:
                if hover:
                    self.muc_dang_chon = i  # đồng bộ hover với bàn phím
                pygame.draw.rect(self.man_hinh, VANG, r, border_radius=12)
                pygame.draw.rect(self.man_hinh, CAM,  r, 3, border_radius=12)
                mau_chu = (25, 25, 25)
            else:
                pygame.draw.rect(self.man_hinh, (35, 35, 75), r, border_radius=12)
                pygame.draw.rect(self.man_hinh, (70, 70, 120), r, 2, border_radius=12)
                mau_chu = TRANG

            chu = self.font_muc.render(nhan, True, mau_chu)
            self.man_hinh.blit(chu, chu.get_rect(center=r.center))



    def xu_ly_su_kien(self, su_kien):
        if su_kien.type == pygame.KEYDOWN:
            if su_kien.key == pygame.K_UP:
                self.muc_dang_chon = (self.muc_dang_chon - 1) % len(self.cac_muc)
            if su_kien.key == pygame.K_DOWN:
                self.muc_dang_chon = (self.muc_dang_chon + 1) % len(self.cac_muc)
            if su_kien.key == pygame.K_RETURN:
                return self.cac_muc[self.muc_dang_chon][1]
            if hasattr(self, 'am_thanh'):
                self.am_thanh.phat_click()

        # Click chuột
        if su_kien.type == pygame.MOUSEBUTTONDOWN and su_kien.button == 1:
            for i, r in enumerate(self.cac_rect_nut):
                if r.collidepoint(su_kien.pos):
                    if hasattr(self, 'am_thanh'):
                        self.am_thanh.phat_click()
                    return self.cac_muc[i][1]

        return TRANG_THAI_MENU
