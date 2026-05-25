# ============================================================
#  main.py — Điểm khởi chạy game
#  F11: toàn màn hình | Cửa sổ resize được
# ============================================================

import pygame, sys, math, time
from cai_dat                  import *
from man_hinh.menu            import Menu
from man_hinh.chon_man        import ChonMan
from man_hinh.man_choi        import ManChoi
from man_hinh.tro_choi_khac   import TroChoiKhac
from man_hinh.thong_tin       import ThongTin
from man_hinh.huong_dan       import HuongDan


# ── Màn hình splash/loading ───────────────────────────────
def _ve_sao_splash(s, cx, cy, r, mau, vien, dem):
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i*36 + dem*0.5)
        ri  = r if i%2==0 else r//2
        pts.append((cx + ri*math.cos(ang), cy + ri*math.sin(ang)))
    pygame.draw.polygon(s, mau, pts)
    pygame.draw.polygon(s, vien, pts, 2)


def _kiem_tra_modules(man_hinh, dong_ho):
    """
    Thực sự import từng module, hiện tiến trình.
    Nếu lỗi → hiện màn đỏ + traceback → chờ Enter rồi thoát.
    Trả về (thanh_cong, man_hinh).
    """
    import traceback, importlib

    SW, SH = 420, 270
    font_label = pygame.font.SysFont(FONT_CHINH, 13)
    font_err   = pygame.font.SysFont(FONT_CHINH, 12)
    font_tieu  = pygame.font.SysFont(FONT_CHINH, 26, bold=True)

    # Danh sách module cần kiểm tra
    CAC_MODULE = [
        ("cai_dat",                     "Cài đặt hằng số..."),
        ("man_hinh.menu",               "Màn hình menu..."),
        ("man_hinh.chon_man",           "Màn chọn màn..."),
        ("man_hinh.huong_dan",          "Màn hướng dẫn..."),
        ("man_hinh.thong_tin",          "Màn thông tin..."),
        ("man_hinh.tro_choi_khac",      "Trò chơi khác..."),
        ("the_gioi.nhan_vat",           "Nhân vật..."),
        ("the_gioi.nen_tang",           "Nền tảng..."),
        ("the_gioi.vat_the",            "Vật thể..."),
        ("the_gioi.boss",               "Boss..."),
        ("the_gioi.tinh_linh",          "Tinh linh..."),
        ("the_gioi.tinh_linh_dieu_khien","Tinh linh điều khiển..."),
        ("tien_ich.camera",             "Camera..."),
        ("tien_ich.hud",                "HUD..."),
        ("tien_ich.man_ket_qua",        "Màn kết quả..."),
        ("tien_ich.hoi_thoai",          "Hội thoại..."),
        ("man_hinh.thoai_cac_man",      "Nội dung thoại..."),
        ("man_hinh.man_choi",           "Màn chơi chính..."),
    ]

    tong = len(CAC_MODULE)

    def _ve_nen(tien_trinh, label, dem):
        man_hinh.fill((14, 14, 34))
        # Viền
        pygame.draw.rect(man_hinh, VANG, (0,0,SW,SH), 2, border_radius=12)
        # Tên game
        t = font_tieu.render(TEN_GAME, True, VANG)
        man_hinh.blit(t, t.get_rect(center=(SW//2, 90)))
        t2 = font_label.render("Đang kiểm tra hệ thống...", True, (130,130,180))
        man_hinh.blit(t2, t2.get_rect(center=(SW//2, 118)))
        # Nhãn bước hiện tại
        tl = font_label.render(label, True, (160,200,220))
        man_hinh.blit(tl, tl.get_rect(center=(SW//2, SH-70)))
        # Thanh tiến trình
        BW,BH = 300,12; bx=(SW-BW)//2; by=SH-50
        pygame.draw.rect(man_hinh,(30,30,60),(bx,by,BW,BH),border_radius=6)
        fw = int(BW*tien_trinh)
        if fw>0:
            r=int(60+195*tien_trinh); g=int(140+70*tien_trinh)
            b_col=max(0,int(220-220*tien_trinh))
            pygame.draw.rect(man_hinh,(r,g,b_col),(bx,by,fw,BH),border_radius=6)
        pygame.draw.rect(man_hinh,(80,80,140),(bx,by,BW,BH),1,border_radius=6)
        # %
        tp = font_label.render(f"{int(tien_trinh*100)}%", True, TRANG)
        man_hinh.blit(tp, tp.get_rect(center=(SW//2, by+BH+14)))
        pygame.display.flip()
        dong_ho.tick(FPS)

    for i, (module_path, label) in enumerate(CAC_MODULE):
        _ve_nen((i+0.5)/tong, label, i)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        try:
            importlib.import_module(module_path)
        except Exception:
            # ── Hiện màn lỗi ──────────────────────────────
            tb = traceback.format_exc()
            man_hinh.fill((20, 5, 5))
            pygame.draw.rect(man_hinh,(200,50,50),(0,0,SW,SH),3,border_radius=10)
            f_err_big = pygame.font.SysFont(FONT_CHINH, 18, bold=True)
            t_err = f_err_big.render("LỖI KHỞI ĐỘNG!", True, (255,80,80))
            man_hinh.blit(t_err, t_err.get_rect(center=(SW//2, 20)))
            t_mod = font_label.render(f"Module: {module_path}", True, (255,200,100))
            man_hinh.blit(t_mod, t_mod.get_rect(center=(SW//2, 45)))
            pygame.draw.line(man_hinh,(150,30,30),(10,58),(SW-10,58),1)
            # In từng dòng traceback
            y = 64
            for line in tb.splitlines():
                line = line.rstrip()
                if not line: continue
                # Cắt nếu quá dài
                while len(line) > 55:
                    t = font_err.render(line[:55], True, (230,180,180))
                    if y < SH - 30:
                        man_hinh.blit(t, (8, y)); y += 14
                    line = "  " + line[55:]
                if y < SH - 30:
                    t = font_err.render(line, True, (230,180,180))
                    man_hinh.blit(t, (8, y)); y += 14
            t_hint = font_label.render("Nhấn Enter hoặc Esc để thoát", True, (150,80,80))
            man_hinh.blit(t_hint, t_hint.get_rect(center=(SW//2, SH-14)))
            pygame.display.flip()
            # Chờ người dùng đóng
            while True:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if ev.type == pygame.KEYDOWN and ev.key in (
                            pygame.K_RETURN, pygame.K_ESCAPE):
                        pygame.quit(); sys.exit()
                dong_ho.tick(30)

    # Tất cả OK — hiện 100% rồi trả về
    _ve_nen(1.0, "Sẵn sàng!", 0)
    import time; time.sleep(0.4)
    return man_hinh


def man_hinh_splash(man_hinh, dong_ho):
    """Splash: kiểm tra module thật, hiện lỗi nếu có."""
    SW, SH = 420, 270
    man_hinh = pygame.display.set_mode((SW, SH))
    pygame.display.set_caption(TEN_GAME + "  —  Đang kiểm tra...")
    return _kiem_tra_modules(man_hinh, dong_ho)


def tao_cac_man(man_hinh):
    return {
        TRANG_THAI_MENU          : Menu(man_hinh),
        TRANG_THAI_CHON_MAN      : ChonMan(man_hinh),
        TRANG_THAI_CHOI          : ManChoi(man_hinh),
        TRANG_THAI_TRO_CHOI_KHAC : TroChoiKhac(man_hinh),
        TRANG_THAI_THONG_TIN     : ThongTin(man_hinh),
        TRANG_THAI_HUONG_DAN     : HuongDan(man_hinh),
    }


def _cap_nhat_man_hinh(cac_man, man_hinh):
    """Cập nhật surface mới cho tất cả màn mà không reset trạng thái."""
    for man in cac_man.values():
        man.man_hinh = man_hinh
        # ManChoi cần cập nhật thêm camera nếu đang chơi
        if hasattr(man, 'camera') and man.camera is not None:
            man.camera.rong_the_gioi = man.camera.rong_the_gioi  # giữ nguyên
        # Gọi resize nếu có (NenMenu)
        if hasattr(man, 'nen') and hasattr(man.nen, 'resize'):
            man.nen.resize(man_hinh)


def chay_game():
    pygame.init()
    dong_ho = pygame.time.Clock()

    # ── Cửa sổ splash nhỏ ────────────────────────────────
    man_hinh = pygame.display.set_mode((420, 270))
    pygame.display.set_caption(TEN_GAME)
    man_hinh = man_hinh_splash(man_hinh, dong_ho)

    # ── Sau splash: mở full màn hình ─────────────────────
    import os
    os.environ.pop('SDL_VIDEO_WINDOW_POS', None)
    man_hinh = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption(TEN_GAME)
    toan_man_hinh = True

    cac_man    = tao_cac_man(man_hinh)
    trang_thai = TRANG_THAI_MENU

    while True:
        man_hien_tai = cac_man[trang_thai]

        for su_kien in pygame.event.get():
            if su_kien.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # F11 fullscreen
            if su_kien.type == pygame.KEYDOWN and su_kien.key == pygame.K_F11:
                import os
                toan_man_hinh = not toan_man_hinh
                if toan_man_hinh:
                    # Xóa env POS để fullscreen không bị offset
                    os.environ.pop('SDL_VIDEO_WINDOW_POS', None)
                    man_hinh = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    # Lấy desktop size khi đang fullscreen (chính xác)
                    info = pygame.display.Info()
                    dw, dh = info.current_w, info.current_h
                    os.environ['SDL_VIDEO_WINDOW_POS'] = (
                        f"{(dw-SCREEN_W)//2},{(dh-SCREEN_H)//2}")
                    man_hinh = pygame.display.set_mode(
                        (SCREEN_W, SCREEN_H), pygame.RESIZABLE)
                _cap_nhat_man_hinh(cac_man, man_hinh)
                continue

            # Resize cửa sổ
            if su_kien.type == pygame.VIDEORESIZE:
                man_hinh = pygame.display.set_mode(
                    (su_kien.w, su_kien.h), pygame.RESIZABLE)
                _cap_nhat_man_hinh(cac_man, man_hinh)
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
