# ============================================================
#  man_hinh/chon_man.py — Chọn màn chơi
# ============================================================

import pygame
from cai_dat import *


class ChonMan:
    def __init__(self, man_hinh):
        self.man_hinh  = man_hinh
        self.dang_chon = 0   # index 0–9 → màn 1–10
        self._tao_font()

    def _tao_font(self):
        w, h = self.man_hinh.get_size()
        self.font_tieude = pygame.font.SysFont(FONT_CHINH, max(24, h // 14), bold=True)
        self.font_so     = pygame.font.SysFont(FONT_CHINH, max(18, h // 22), bold=True)
        self.font_nhan   = pygame.font.SysFont(FONT_CHINH, max(12, h // 36))

    def lay_man_dang_chon(self):
        return self.dang_chon + 1   # trả về số màn 1–10

    def update(self):
        self._tao_font()

    def ve(self):
        w, h = self.man_hinh.get_size()
        self.man_hinh.fill((18, 18, 40))
        self.cac_rect = []

        tieu = self.font_tieude.render("Chon Man Choi", True, VANG)
        ty   = h // 12
        self.man_hinh.blit(tieu, tieu.get_rect(center=(w//2, ty)))
        pygame.draw.line(self.man_hinh, (60, 60, 120),
                         (w//2 - 180, ty + 22), (w//2 + 180, ty + 22), 1)

        COT, HANG = 5, 2
        le_trai = w * 0.07;  le_phai = w * 0.07
        le_tren = h * 0.22;  le_duoi = h * 0.12
        khoang  = w * 0.02
        o_c = (w - le_trai - le_phai - khoang*(COT-1)) / COT
        o_r = (h - le_tren - le_duoi - khoang*(HANG-1)) / HANG

        mx, my = pygame.mouse.get_pos()

        for i in range(10):
            hi = i // COT;  ci = i % COT
            x  = int(le_trai + ci * (o_c + khoang))
            y  = int(le_tren + hi * (o_r + khoang))
            r  = pygame.Rect(x, y, int(o_c), int(o_r))
            self.cac_rect.append(r)

            so_man    = i + 1
            boss_cuoi = (so_man == 10)
            la_boss   = (so_man == 5)
            hover     = r.collidepoint(mx, my)
            chon      = (i == self.dang_chon)
            if hover: self.dang_chon = i

            if boss_cuoi:
                mau_nen  = (70, 0, 0)
                mau_vien = (255, 60, 60) if (chon or hover) else (140, 20, 20)
                day      = 3
            elif la_boss:
                mau_nen  = (55, 28, 0)
                mau_vien = VANG if (chon or hover) else CAM
                day      = 3
            else:
                mau_nen  = (40, 40, 85) if (chon or hover) else (28, 28, 60)
                mau_vien = VANG if (chon or hover) else (65, 65, 120)
                day      = 2 if (chon or hover) else 1

            pygame.draw.rect(self.man_hinh, mau_nen,  r, border_radius=10)
            pygame.draw.rect(self.man_hinh, mau_vien, r, day, border_radius=10)

            mau_so = (255,90,90) if boss_cuoi else (255,180,60) if la_boss else TRANG
            t_so   = self.font_so.render(f"Man {so_man}", True, mau_so)
            self.man_hinh.blit(t_so, t_so.get_rect(center=r.center))

            if boss_cuoi:
                nb = self.font_nhan.render("BOSS CUOI", True, (255,80,80))
                self.man_hinh.blit(nb, nb.get_rect(
                    center=(r.centerx, r.bottom - int(o_r*0.18))))
            elif la_boss:
                nb = self.font_nhan.render("BOSS", True, CAM)
                self.man_hinh.blit(nb, nb.get_rect(
                    center=(r.centerx, r.bottom - int(o_r*0.18))))

    def xu_ly_su_kien(self, su_kien):
        if su_kien.type == pygame.KEYDOWN:
            if su_kien.key == pygame.K_RIGHT: self.dang_chon = (self.dang_chon+1)%10
            if su_kien.key == pygame.K_LEFT:  self.dang_chon = (self.dang_chon-1)%10
            if su_kien.key == pygame.K_DOWN:  self.dang_chon = (self.dang_chon+5)%10
            if su_kien.key == pygame.K_UP:    self.dang_chon = (self.dang_chon-5)%10
            if su_kien.key == pygame.K_RETURN:  return TRANG_THAI_CHOI
            if su_kien.key == pygame.K_ESCAPE:  return TRANG_THAI_MENU
        if su_kien.type == pygame.MOUSEBUTTONDOWN and su_kien.button == 1:
            for i, r in enumerate(self.cac_rect):
                if r.collidepoint(su_kien.pos):
                    self.dang_chon = i
                    return TRANG_THAI_CHOI
        return TRANG_THAI_CHON_MAN
