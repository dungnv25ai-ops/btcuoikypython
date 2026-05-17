# ============================================================
#  main.py — Điểm khởi chạy game
#  F11: toàn màn hình | Cửa sổ resize được
# ============================================================

import pygame, sys
from cai_dat                  import *
from man_hinh.menu            import Menu
from man_hinh.chon_man        import ChonMan
from man_hinh.man_choi        import ManChoi
from man_hinh.tro_choi_khac   import TroChoiKhac
from man_hinh.thong_tin       import ThongTin
from man_hinh.huong_dan       import HuongDan


def tao_cac_man(man_hinh):
    return {
        TRANG_THAI_MENU          : Menu(man_hinh),
        TRANG_THAI_CHON_MAN      : ChonMan(man_hinh),
        TRANG_THAI_CHOI          : ManChoi(man_hinh),
        TRANG_THAI_TRO_CHOI_KHAC : TroChoiKhac(man_hinh),
        TRANG_THAI_THONG_TIN     : ThongTin(man_hinh),
        TRANG_THAI_HUONG_DAN     : HuongDan(man_hinh),
    }


def chay_game():
    pygame.init()
    man_hinh = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.RESIZABLE)
    pygame.display.set_caption(TEN_GAME)
    dong_ho       = pygame.time.Clock()
    toan_man_hinh = False

    cac_man    = tao_cac_man(man_hinh)
    trang_thai = TRANG_THAI_MENU

    while True:
        man_hien_tai = cac_man[trang_thai]

        for su_kien in pygame.event.get():
            if su_kien.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # F11 fullscreen
            if su_kien.type == pygame.KEYDOWN and su_kien.key == pygame.K_F11:
                toan_man_hinh = not toan_man_hinh
                flags = pygame.FULLSCREEN if toan_man_hinh else pygame.RESIZABLE
                size  = (0, 0) if toan_man_hinh else (SCREEN_W, SCREEN_H)
                man_hinh = pygame.display.set_mode(size, flags)
                cac_man  = tao_cac_man(man_hinh)
                continue

            # Resize cửa sổ
            if su_kien.type == pygame.VIDEORESIZE:
                man_hinh = pygame.display.set_mode(
                    (su_kien.w, su_kien.h), pygame.RESIZABLE)
                cac_man = tao_cac_man(man_hinh)
                continue

            trang_thai_moi = man_hien_tai.xu_ly_su_kien(su_kien)

            # Khi chuyển sang màn chơi → báo số màn đã chọn
            if (trang_thai_moi == TRANG_THAI_CHOI
                    and trang_thai == TRANG_THAI_CHON_MAN):
                so_man = cac_man[TRANG_THAI_CHON_MAN].lay_man_dang_chon()
                cac_man[TRANG_THAI_CHOI].tai_man(so_man)

            if trang_thai_moi != trang_thai:
                trang_thai = trang_thai_moi

        man_hien_tai.update()
        man_hien_tai.ve()
        pygame.display.flip()
        dong_ho.tick(FPS)


if __name__ == "__main__":
    chay_game()
