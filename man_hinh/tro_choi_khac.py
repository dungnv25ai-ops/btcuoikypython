# ============================================================
#  man_hinh/tro_choi_khac.py — Trò chơi khác (placeholder)
# ============================================================

import pygame
from cai_dat import *


class TroChoiKhac:
    def __init__(self, man_hinh):
        self.man_hinh = man_hinh

    def _tao_font(self):
        w, h = self.man_hinh.get_size()
        self.font_to  = pygame.font.SysFont(FONT_CHINH, max(30, h // 13), bold=True)
        self.font_nho = pygame.font.SysFont(FONT_CHINH, max(16, h // 28))

    def update(self):
        self._tao_font()

    def ve(self):
        w, h = self.man_hinh.get_size()
        self._tao_font()
        self.man_hinh.fill((18, 18, 40))

        pygame.draw.rect(self.man_hinh, (35, 35, 75),
                         (w*0.1, h*0.15, w*0.8, h*0.7), border_radius=16)
        pygame.draw.rect(self.man_hinh, (60, 60, 120),
                         (w*0.1, h*0.15, w*0.8, h*0.7), 2, border_radius=16)

        tieu = self.font_to.render("Trò Chơi Khác", True, VANG)
        phu  = self.font_nho.render("Đang phát triển — Sắp ra mắt!", True, XAM)
        esc  = self.font_nho.render("ESC: Quay lại", True, (70, 70, 110))

        self.man_hinh.blit(tieu, tieu.get_rect(center=(w//2, h*0.42)))
        self.man_hinh.blit(phu,  phu.get_rect(center=(w//2, h*0.55)))
        self.man_hinh.blit(esc,  esc.get_rect(center=(w//2, h*0.78)))

    def xu_ly_su_kien(self, su_kien):
        if su_kien.type == pygame.KEYDOWN and su_kien.key == pygame.K_ESCAPE:
            return TRANG_THAI_MENU
        if su_kien.type == pygame.MOUSEBUTTONDOWN:
            return TRANG_THAI_MENU
        return TRANG_THAI_TRO_CHOI_KHAC
