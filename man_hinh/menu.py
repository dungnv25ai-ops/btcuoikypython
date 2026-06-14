# ============================================================
#  man_hinh/menu.py — Menu chính
#  Nền: tai_nguyen/hinh_anh/menu.png
#  4 bảng gỗ bên phải — text đè lên
# ============================================================

import pygame, os
from cai_dat import *

# ── Vị trí 4 bảng gỗ (tỉ lệ so với kích thước màn hình) ──
# Đo lại từ ảnh thực tế 1512×756:
#   bảng 1: y≈7%,  bảng 2: y≈28%, bảng 3: y≈49%, bảng 4: y≈70%
#   x bắt đầu ≈53%, rộng ≈44%,  cao mỗi bảng ≈17%
_BANG_GO = [
    (0.560, 0.120, 0.380, 0.160),  # Bảng 1
    (0.560, 0.320, 0.380, 0.160),  # Bảng 2
    (0.560, 0.520, 0.380, 0.160),  # Bảng 3
    (0.560, 0.720, 0.380, 0.160),  # Bảng 4
]

_CACHE_NEN = {}


def _load_nen(man_hinh):
    w, h = man_hinh.get_size()
    if (w, h) in _CACHE_NEN:
        return _CACHE_NEN[(w, h)]
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'tai_nguyen', 'hinh_anh', 'menu.png')
    surf = None
    if os.path.isfile(path):
        try:
            img  = pygame.image.load(path).convert()
            surf = pygame.transform.scale(img, (w, h))
        except Exception:
            pass
    _CACHE_NEN[(w, h)] = surf
    return surf


class Menu:
    def __init__(self, man_hinh):
        self.man_hinh      = man_hinh
        self.muc_dang_chon = 0
        self.cac_rect_nut  = []
        self._dem          = 0   # đếm frame cho animation

        self.cac_muc = [
            ("Chọn màn",           TRANG_THAI_CHON_MAN),
            ("Trò chơi khác",      TRANG_THAI_TRO_CHOI_KHAC),
            ("Hướng dẫn",          TRANG_THAI_HUONG_DAN),
            ("Thông tin trò chơi", TRANG_THAI_THONG_TIN),
        ]
        self._tao_font()

    def _tao_font(self):
        w, h = self.man_hinh.get_size()
        co = max(22, int(h * _BANG_GO[0][3] * 0.42))
        self.font_muc = pygame.font.SysFont(FONT_CHINH, co, bold=True)

    def update(self):
        self._tao_font()
        self._dem += 1

    def ve(self):
        import math
        w, h = self.man_hinh.get_size()
        self.cac_rect_nut = []

        # ── Nền ─────────────────────────────────────────
        nen = _load_nen(self.man_hinh)
        if nen:
            self.man_hinh.blit(nen, (0, 0))
        else:
            self.man_hinh.fill((18, 18, 40))

        mx, my = pygame.mouse.get_pos()

        for i, (nhan, _) in enumerate(self.cac_muc):
            xr, yr, wr, hr = _BANG_GO[i]
            bx = int(w * xr)
            by = int(h * yr)
            bw = int(w * wr)
            bh = int(h * hr)
            r  = pygame.Rect(bx, by, bw, bh)
            self.cac_rect_nut.append(r)

            hover = r.collidepoint(mx, my)
            chon  = (i == self.muc_dang_chon)
            if hover:
                self.muc_dang_chon = i

            active = chon or hover

            # ── Highlight bên trong bảng khi hover/chọn ──
            # ── Highlight khi hover/chọn (Chỉ đổi màu chữ) ──
            if active:
                mau_chu  = (255, 235, 150)  # Vàng sáng nổi bật khi trỏ chuột
                mau_bong = (100, 50, 10)    # Bóng tối đậm để chữ pop-up lên
            else:
                mau_chu  = (80, 45, 20)     # Nâu gỗ tối chìm vào bảng
                mau_bong = (220, 190, 150)  # Bóng sáng mờ giả hiệu ứng khắc gỗ

            # ── Text canh giữa bảng ───────────────────────
            cx = bx + bw // 2
            cy = by + bh // 2
            bong = self.font_muc.render(nhan, True, mau_bong)
            chu  = self.font_muc.render(nhan, True, mau_chu)
            
            self.man_hinh.blit(bong, bong.get_rect(center=(cx+2, cy+2)))
            self.man_hinh.blit(chu,  chu.get_rect(center=(cx, cy)))

    def xu_ly_su_kien(self, su_kien):
        if su_kien.type == pygame.KEYDOWN:
            if su_kien.key == pygame.K_UP:
                self.muc_dang_chon = (self.muc_dang_chon - 1) % len(self.cac_muc)
            if su_kien.key == pygame.K_DOWN:
                self.muc_dang_chon = (self.muc_dang_chon + 1) % len(self.cac_muc)
            if su_kien.key == pygame.K_RETURN:
                return self.cac_muc[self.muc_dang_chon][1]

        if su_kien.type == pygame.MOUSEBUTTONDOWN and su_kien.button == 1:
            for i, r in enumerate(self.cac_rect_nut):
                if r.collidepoint(su_kien.pos):
                    return self.cac_muc[i][1]

        return TRANG_THAI_MENU