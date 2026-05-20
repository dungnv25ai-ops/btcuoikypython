# ============================================================
#  main.py — Điểm khởi chạy game
#  F11: toàn màn hình | Cửa sổ resize được
# ============================================================

import pygame, sys,math, time
from cai_dat                  import *
from man_hinh.menu            import Menu
from man_hinh.chon_man        import ChonMan
from man_hinh.man_choi        import ManChoi
from man_hinh.tro_choi_khac   import TroChoiKhac
from man_hinh.thong_tin       import ThongTin
from man_hinh.huong_dan       import HuongDan
def _cap_nhat_man_hinh(cac_man, man_hinh):
    """Cập nhật surface mới cho tất cả màn mà không reset trạng thái."""
    for man in cac_man.values():
        man.man_hinh = man_hinh
        # ManChoi cần cập nhật thêm camera nếu đang chơi
        if hasattr(man, 'camera') and man.camera is not None:
            man.camera.rong_the_gioi  
        # Gọi resize nếu có (NenMenu)
        if hasattr(man, 'nen') and hasattr(man.nen, 'resize'):
            man.nen.resize(man_hinh)
def _ve_sao_splash(s, cx, cy, r, mau, vien, dem):
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i*36 + dem*0.5)
        ri  = r if i%2==0 else r//2
        pts.append((cx + ri*math.cos(ang), cy + ri*math.sin(ang)))
    pygame.draw.polygon(s, mau, pts)
    pygame.draw.polygon(s, vien, pts, 2)
def man_hinh_splash(man_hinh, dong_ho):
    """
    Splash nhỏ: cửa sổ 400×260, hiện logo + thanh load,
    sau ~2.5s tự chuyển sang game.
    Nhấn bất kỳ phím / click → bỏ qua.
    """
    SW, SH = 420, 270
    # Resize cửa sổ về kích thước nhỏ
    man_hinh = pygame.display.set_mode((SW, SH))
    pygame.display.set_caption(TEN_GAME + "  —  Đang tải...")

    font_ten  = pygame.font.SysFont(FONT_CHINH, 26, bold=True)
    font_sub  = pygame.font.SysFont(FONT_CHINH, 13)
    font_pct  = pygame.font.SysFont(FONT_CHINH, 14, bold=True)

    # Các bước giả lập loading
    BUOC = [
        (0.18, "Khởi tạo Pygame..."),
        (0.35, "Tải màn hình..."),
        (0.52, "Tải nhân vật..."),
        (0.68, "Tải bản đồ..."),
        (0.82, "Tải âm thanh..."),
        (1.00, "Sẵn sàng!"),
    ]
    TONG_FRAMES = int(FPS * 2.6)   # ~2.6 giây

    dem = 0
    for frame in range(TONG_FRAMES + 1):
        # Thoát sớm
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return man_hinh   # skip

        tien_trinh = frame / TONG_FRAMES
        dem += 1

        # ── Nền ──────────────────────────────────────────
        man_hinh.fill((14, 14, 34))

        # Viền cửa sổ phát sáng
        a_vien = int(120 + 80*abs(math.sin(dem*0.05)))
        pygame.draw.rect(man_hinh, (*VANG[:3], a_vien),
                         (0, 0, SW, SH), 3, border_radius=12)

        # ── 3 sao nhỏ xoay ───────────────────────────────
        for i, (sx, sy, sr) in enumerate([(70,80,14),(SW//2,60,10),(SW-70,80,14)]):
            a_sao = int(180 + 75*abs(math.sin(dem*0.07+i)))
            gs = pygame.Surface((sr*2+4, sr*2+4), pygame.SRCALPHA)
            _ve_sao_splash(gs, sr+2, sr+2, sr,
                           (255,210,0), (255,240,100), dem+i*40)
            gs.set_alpha(a_sao)
            man_hinh.blit(gs, (sx-sr-2, sy-sr-2))

        # ── Tên game ──────────────────────────────────────
        t_bong = font_ten.render(TEN_GAME, True, (0,0,0))
        t_ten  = font_ten.render(TEN_GAME, True, VANG)
        man_hinh.blit(t_bong, t_bong.get_rect(center=(SW//2+2, 118)))
        man_hinh.blit(t_ten,  t_ten.get_rect(center=(SW//2, 116)))

        # ── Dòng phụ ──────────────────────────────────────
        t_sub = font_sub.render("Python + Pygame  |  2D Puzzle Platformer",
                                True, (130,130,180))
        man_hinh.blit(t_sub, t_sub.get_rect(center=(SW//2, 138)))

        # ── Thanh tiến trình ──────────────────────────────
        BW, BH = 300, 14
        bx = (SW-BW)//2; by = SH - 58
        # Nền thanh
        pygame.draw.rect(man_hinh, (30,30,60), (bx,by,BW,BH), border_radius=7)
        # Thanh đầy
        fill_w = int(BW * tien_trinh)
        if fill_w > 0:
            # Gradient đơn giản: xanh → vàng
            r = int(60 + 195*tien_trinh)
            g = int(140 + 70*tien_trinh)
            b_col = max(0, int(220 - 220*tien_trinh))
            pygame.draw.rect(man_hinh, (r,g,b_col),
                             (bx, by, fill_w, BH), border_radius=7)
            # Glow đầu thanh
            gx = bx + fill_w
            gs2 = pygame.Surface((20, BH), pygame.SRCALPHA)
            for xi in range(20):
                alpha = int(180*(1-xi/20))
                pygame.draw.line(gs2, (255,255,255,alpha),
                                 (20-xi, 0), (20-xi, BH))
            man_hinh.blit(gs2, (gx-20, by))
        pygame.draw.rect(man_hinh, (80,80,140), (bx,by,BW,BH), 2, border_radius=7)

        # ── Label bước hiện tại ───────────────────────────
        label = BUOC[0][1]
        for nguong, txt in BUOC:
            if tien_trinh >= nguong - 0.01: label = txt
        t_label = font_sub.render(label, True, (160,170,220))
        man_hinh.blit(t_label, t_label.get_rect(center=(SW//2, by-14)))

        # ── Phần trăm ─────────────────────────────────────
        t_pct = font_pct.render(f"{int(tien_trinh*100)}%", True, TRANG)
        man_hinh.blit(t_pct, t_pct.get_rect(center=(SW//2, by+BH+14)))

        # ── Nhấn phím bỏ qua ──────────────────────────────
        if frame < TONG_FRAMES - 10:
            t_skip = font_sub.render("Nhấn phím bất kỳ để bỏ qua", True, (60,60,100))
            man_hinh.blit(t_skip, t_skip.get_rect(center=(SW//2, SH-10)))

        pygame.display.flip()
        dong_ho.tick(FPS)

    # Giữ màn "Sẵn sàng!" thêm 0.4s
    time.sleep(0.4)
    return man_hinh


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
    dong_ho = pygame.time.Clock()

    # ── Cửa sổ splash nhỏ ────────────────────────────────
    man_hinh = pygame.display.set_mode((420, 270))
    pygame.display.set_caption(TEN_GAME)
    man_hinh = man_hinh_splash(man_hinh, dong_ho)
    man_hinh = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption(TEN_GAME)
    toan_man_hinh = True

    cac_man    = tao_cac_man(man_hinh)
    trang_thai = TRANG_THAI_MENU
    from tien_ich.am_thanh import AmThanh
    am_thanh = AmThanh()
    cac_man[TRANG_THAI_MENU].am_thanh = am_thanh
    cac_man[TRANG_THAI_CHOI].am_thanh = am_thanh

    # Bật nhạc menu khi game vừa mở
    am_thanh.choi_nhac("menu")

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
                _cap_nhat_man_hinh(cac_man, man_hinh)
                continue

            # Resize cửa sổ
            if su_kien.type == pygame.VIDEORESIZE:
                man_hinh = pygame.display.set_mode(
                    (su_kien.w, su_kien.h), pygame.RESIZABLE)
                _cap_nhat_man_hinh(cac_man, man_hinh)
                continue

            trang_thai_moi = man_hien_tai.xu_ly_su_kien(su_kien)

            # ==========================================
            # LOGIC CHUYỂN MÀN CHƠI -> ĐỔI SANG NHẠC GAME
            # ==========================================
            if (trang_thai_moi == TRANG_THAI_CHOI
                    and trang_thai == TRANG_THAI_CHON_MAN):
                so_man = cac_man[TRANG_THAI_CHON_MAN].lay_man_dang_chon()
                cac_man[TRANG_THAI_CHOI].tai_man(so_man)
                
                # Ra lệnh đổi nhạc tùy theo màn đang chọn
                # Nếu là các màn thông thường, bật nhạc màn
                if so_man == 5:
                    am_thanh.choi_nhac("boss_5")
                elif so_man == 10:
                    am_thanh.choi_nhac("boss_10_p1")
                elif 6 <= so_man <= 9:
                    am_thanh.choi_nhac("man_6_9")
                else:
                    am_thanh.choi_nhac("man_1_4") 

            # ==========================================
            # LOGIC QUAY LẠI MENU -> TRỞ VỀ NHẠC MENU
            # ==========================================
            if trang_thai_moi == TRANG_THAI_MENU and trang_thai != TRANG_THAI_MENU:
                am_thanh.choi_nhac("menu")

            if trang_thai_moi != trang_thai:
                trang_thai = trang_thai_moi

        man_hien_tai.update()
        man_hien_tai.ve()
        pygame.display.flip()
        dong_ho.tick(FPS)


if __name__ == "__main__":
    chay_game()
