# ============================================================
#  man_hinh/tro_choi_khac.py
#  Hoàn toàn độc lập với man_choi.py
#
#  Lớp 1 — chọn loại: Mê Cung | PvE
#  Lớp 2 — chọn màn 1-10
#  Lớp 3 — chơi game (ManChoiKhac tự xử lý)
# ============================================================

import pygame
import math
from cai_dat import *
from tien_ich.nut_back import ve_nut_back as _ve_nut_back, ve_nen_chung
from man_hinh.mapMC import lay_map_me_cung
from man_hinh.mapPE import lay_map_pve
from the_gioi.nen_tang  import NenTang, TileCo, ODict, TileLa, KhoiTanHinh, SaoMap
from the_gioi.tinh_linh_dieu_khien import TinhLinhDieuKhien
from the_gioi.vat_the   import Gai, KhoiNuoc
from tien_ich.camera    import Camera
from tien_ich.hud       import HUD
from tien_ich.man_ket_qua import ManKetQua
from tien_ich.hoi_thoai   import HoiThoai, ThongBao

T = TILE_SIZE

# ── Trạng thái nội bộ ─────────────────────────────────────
_LOP_CHON_LOAI = 'chon_loai'
_LOP_CHON_MAN  = 'chon_man'
_LOP_SAP_RA    = 'sap_ra'
_LOP_CHOI      = 'choi'


# ══════════════════════════════════════════════════════════
#  ManChoiKhac — game loop riêng cho mê cung và pve
# ══════════════════════════════════════════════════════════
class ManChoiKhac:
    """Màn chơi độc lập cho TroChoiKhac.
    - Mê cung: zoom full map + bóng tối + tinh linh điều khiển
    - PvE:     zoom full map (giống boss 5/10, chưa có boss riêng)
    """
    def __init__(self, man_hinh):
        self.man_hinh   = man_hinh
        self.loai       = None   # 'me_cung' | 'pve'
        self.so_man     = 1
        self.hud        = HUD()
        self.ket_qua    = ManKetQua()
        self.hoi_thoai  = HoiThoai()
        self.thong_bao  = ThongBao()
        self.camera     = None
        self.tam_dung   = False
        self.da_thang   = False
        self._muc_pause = 0
        self._tao_font()

    def _tao_font(self):
        w, h = self.man_hinh.get_size()
        self.fm = pygame.font.SysFont(FONT_CHINH, max(18, h//24), bold=True)
        self.fn = pygame.font.SysFont(FONT_CHINH, max(13, h//36))

    # ── Load màn ──────────────────────────────────────────
    def tai_man(self, loai, so_man):
        self.loai    = loai
        self.so_man  = so_man
        self.hud.reset()
        self.ket_qua.an()
        self.hoi_thoai = HoiThoai()
        self.thong_bao = ThongBao()
        self.da_thang  = False
        self.tam_dung  = False
        self._tai_ban_do()

    def _tai_ban_do(self):
        if self.loai == 'me_cung':
            ban_do = lay_map_me_cung(self.so_man)
        else:
            ban_do = lay_map_pve(self.so_man)

        if ban_do is None:
            # Map chưa có — tạo map trống tối thiểu để không crash
            ban_do = [
                "####",
                "#P *",
                "####",
            ]

        self.ban_do  = ban_do
        self.ds_nen  = pygame.sprite.Group()
        self.ds_dich = pygame.sprite.Group()
        self.ds_roi  = pygame.sprite.Group()
        self.ds_nuoc = pygame.sprite.Group()
        self.ds_sao  = pygame.sprite.Group()
        self.ds_la   = pygame.sprite.Group()
        self._man9_tl = None   # tinh linh điều khiển (mê cung)
        sx = sy = 0

        KHOI_DUNG = ('#', 'C', '~', 'W')
        for ri, hang in enumerate(ban_do):
            for ci, o in enumerate(hang):
                if   o == '#': self.ds_nen.add(NenTang(ci, ri))
                elif o == 'T': self.ds_nen.add(KhoiTanHinh(ci, ri))
                elif o == 'C': self.ds_nen.add(TileCo(ci, ri))
                elif o == '~': self.ds_nuoc.add(KhoiNuoc(ci, ri))
                elif o == 'R': self.ds_roi.add(Gai(ci, ri))
                elif o == '$': self.ds_sao.add(SaoMap(ci, ri))
                elif o == '*': self.ds_dich.add(ODict(ci, ri))
                elif o == 'P': sx, sy = ci, ri

        # Spawn TileLa phía trên tile C
        for ri, hang in enumerate(ban_do):
            for ci, o in enumerate(hang):
                if o == 'C':
                    o_tren = ban_do[ri-1][ci] if ri > 0 else ' '
                    if o_tren not in KHOI_DUNG:
                        self.ds_la.add(TileLa(ci, ri))

        # Tinh linh (mê cung) hoặc dummy ngoài màn (pve)
        if self.loai == 'me_cung':
            self._man9_tl = TinhLinhDieuKhien(sx*T, sy*T)
        else:
            self._man9_tl = TinhLinhDieuKhien(-9999, -9999)

        self.spawn_x = sx * T
        self.spawn_y = sy * T

        rong = len(ban_do[0]) * T
        cao  = len(ban_do)    * T
        self.camera = Camera(rong, cao)
        self.camera.cap_nhat_boss(
            *self.man_hinh.get_size())

    # ── Update ────────────────────────────────────────────
    def update(self):
        self._tao_font()
        if self.tam_dung or self.ket_qua.hien:
            return

        self.hoi_thoai.update()
        self.thong_bao.update()
        if self.hoi_thoai.dang_hien or self.thong_bao.dang_hien:
            return

        # Update camera cố định
        w, h = self.man_hinh.get_size()
        self.camera.cap_nhat_boss(w, h)

        # Update sprite
        self.ds_nuoc.update()
        self.ds_sao.update()
        self.ds_la.update()

        if self._man9_tl:
            self._man9_tl.update(list(self.ds_nen))

            # Nhặt sao
            for s in list(self.ds_sao):
                if self._man9_tl.rect.colliderect(s.rect):
                    self.ds_sao.remove(s)
                    self.hud.nhat_sao()

            # Tới đích
            for d in self.ds_dich:
                if self._man9_tl.rect.colliderect(d.rect):
                    self.da_thang = True
                    self.ket_qua.hien_thang(self.so_man, self.hud.sao)
                    break

            # Gai
            for g in self.ds_roi:
                if g.kiem_tra_cham_nguoi(self._man9_tl.rect):
                    go = self.hud.mat_mang()
                    self._man9_tl.x = float(self.spawn_x)
                    self._man9_tl.y = float(self.spawn_y)
                    if go:
                        self.ket_qua.hien_thua(self.so_man)
                    break

    # ── Vẽ ────────────────────────────────────────────────
    def ve(self):
        w, h = self.man_hinh.get_size()
        cam   = self.camera
        ty_le = cam.ty_le

        # Tạo canvas kích thước map
        map_w = int(cam.rong_the_gioi)
        map_h = int(cam.cao_the_gioi)
        canvas = pygame.Surface((map_w, map_h))

        if self.loai == 'me_cung':
            canvas.fill((0, 0, 0))
        else:
            canvas.fill((35, 15, 15))

        # Vẽ tile
        for s in [*self.ds_nen, *self.ds_dich, *self.ds_roi]:
            canvas.blit(s.image, s.rect)
        for n in self.ds_nuoc:
            canvas.blit(n.image, n.rect)
        for la in self.ds_la:
            canvas.blit(la.image, la.rect)
        for s in self.ds_sao:
            canvas.blit(s.image, s.rect)

        if self._man9_tl:
            if self.loai == 'me_cung':
                # Vẽ tinh linh
                self._man9_tl.ve(canvas, 0, 0)
                # Bóng tối
                tx  = int(self._man9_tl.rect.centerx)
                ty9 = int(self._man9_tl.rect.centery)
                R   = T + T//2
                dark = pygame.Surface((map_w, map_h), pygame.SRCALPHA)
                dark.fill((0, 0, 0, 245))
                for rv in [R, int(R*0.7), int(R*0.4)]:
                    pygame.draw.circle(dark, (0,0,0,0), (tx, ty9), rv)
                for rv in range(R, R+12):
                    pygame.draw.circle(dark, (0,0,0,int(245*(rv-R)/12)),
                                       (tx, ty9), rv, 1)
                canvas.blit(dark, (0, 0))

        # Scale canvas → màn hình
        sw     = int(map_w * ty_le)
        sh     = int(map_h * ty_le)
        scaled = pygame.transform.scale(canvas, (sw, sh))
        ox = (w - sw) // 2
        oy = (h - sh) // 2
        self.man_hinh.fill((0, 0, 0))
        self.man_hinh.blit(scaled, (max(0, ox), max(0, oy)))

        # HUD + nút + overlay
        self.hud.ve_don_gian(self.man_hinh)
        self._ve_nut(w)
        self.ket_qua.ve(self.man_hinh)
        self.hoi_thoai.ve(self.man_hinh)
        self.thong_bao.ve(self.man_hinh)
        if self.tam_dung:
            self._ve_pause(w, h)

    NUT_S = 36; NUT_P = 8

    def _ve_nut(self, w):
        s = self.NUT_S; p = self.NUT_P
        self.r_pause = pygame.Rect(w-s-p, p, s, s)
        pygame.draw.rect(self.man_hinh, (30,30,30), self.r_pause, border_radius=8)
        pygame.draw.rect(self.man_hinh, (180,180,180), self.r_pause, 2, border_radius=8)
        cx, cy = self.r_pause.center
        pygame.draw.rect(self.man_hinh, TRANG, (cx-9, cy-10, 7, 20))
        pygame.draw.rect(self.man_hinh, TRANG, (cx+2,  cy-10, 7, 20))

    MUC_P = [("Tiep tuc","tc"), ("Choi lai","cl"), ("Ve menu chon man","vm")]

    def _ve_pause(self, w, h):
        ov = pygame.Surface((w, h), pygame.SRCALPHA)
        ov.fill((0,0,0,160)); self.man_hinh.blit(ov, (0,0))
        ft = pygame.font.SysFont(FONT_CHINH, max(30,h//12), bold=True)
        ti = ft.render("Tam Dung", True, VANG)
        self.man_hinh.blit(ti, ti.get_rect(center=(w//2, h//2-100)))
        self.r_mp = []
        nw = min(320, w-80); nr = max(40, h//14)
        for i, (nhan, _) in enumerate(self.MUC_P):
            y = h//2-30 + i*(nr+10)
            r = pygame.Rect(w//2-nw//2, y, nw, nr)
            self.r_mp.append(r)
            pygame.draw.rect(self.man_hinh,
                             VANG if i==self._muc_pause else (40,40,80),
                             r, border_radius=10)
            pygame.draw.rect(self.man_hinh,
                             CAM  if i==self._muc_pause else (70,70,130),
                             r, 2, border_radius=10)
            chu = self.fm.render(nhan, True,
                                 (25,25,25) if i==self._muc_pause else TRANG)
            self.man_hinh.blit(chu, chu.get_rect(center=r.center))

    # ── Sự kiện ───────────────────────────────────────────
    def xu_ly_su_kien(self, ev):
        if self.ket_qua.hien:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                w2, h2 = self.man_hinh.get_size()
                ket = self.ket_qua.xu_ly_click(ev.pos, w2, h2)
                if ket == 'choi_lai':
                    self.tai_man(self.loai, self.so_man)
                elif ket == 'man_tiep':
                    ban_do = lay_map_me_cung(self.so_man+1) if self.loai == 'me_cung' \
                             else lay_map_pve(self.so_man+1)
                    if ban_do and self.so_man < 10:
                        self.tai_man(self.loai, self.so_man+1)
                    else:
                        return 've_chon_man'
                elif ket == 'man_chinh':
                    return 've_chon_man'
            return None

        if self.hoi_thoai.dang_hien:
            self.hoi_thoai.xu_ly(ev); return None
        if self.thong_bao.dang_hien:
            self.thong_bao.xu_ly(ev); return None

        if ev.type == pygame.KEYDOWN:
            if self.tam_dung:
                if ev.key == pygame.K_UP:
                    self._muc_pause = (self._muc_pause-1) % len(self.MUC_P)
                if ev.key == pygame.K_DOWN:
                    self._muc_pause = (self._muc_pause+1) % len(self.MUC_P)
                if ev.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return self._do_pause()
                return None
            if ev.key == pygame.K_ESCAPE:
                self.tam_dung = True; self._muc_pause = 0
            if ev.key == pygame.K_r:
                self.tai_man(self.loai, self.so_man)

        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if hasattr(self, 'r_pause') and self.r_pause.collidepoint(ev.pos):
                self.tam_dung = not self.tam_dung; self._muc_pause = 0
                return None
            if self.tam_dung and hasattr(self, 'r_mp'):
                for i, r in enumerate(self.r_mp):
                    if r.collidepoint(ev.pos):
                        self._muc_pause = i; return self._do_pause()

        if ev.type == pygame.MOUSEMOTION:
            if self.tam_dung and hasattr(self, 'r_mp'):
                for i, r in enumerate(self.r_mp):
                    if r.collidepoint(ev.pos): self._muc_pause = i
        return None

    def _do_pause(self):
        a = self.MUC_P[self._muc_pause][1]
        if a == 'tc':  self.tam_dung = False
        elif a == 'cl': self.tai_man(self.loai, self.so_man)
        elif a == 'vm': self.tam_dung = False; return 've_chon_man'
        return None


# ══════════════════════════════════════════════════════════
#  Sao trên map (copy nhẹ từ man_choi)
# ══════════════════════════════════════════════════════════
#  TroChoiKhac — màn hình chính (menu chọn loại + chọn màn)
# ══════════════════════════════════════════════════════════
class TroChoiKhac:
    def __init__(self, man_hinh):
        self.man_hinh  = man_hinh
        self._lop      = _LOP_CHON_LOAI
        self._loai     = None
        self._man_chon = 0
        self._r_loai   = []
        self._r_man    = []
        self._r_back   = None
        self._game     = ManChoiKhac(man_hinh)

    def _tao_font(self):
        w, h = self.man_hinh.get_size()
        self.ft = pygame.font.SysFont(FONT_CHINH, max(26,h//14), bold=True)
        self.fm = pygame.font.SysFont(FONT_CHINH, max(18,h//22), bold=True)
        self.fn = pygame.font.SysFont(FONT_CHINH, max(13,h//36))

    # ── Tự động tính màn nào có map ───────────────────────
    def _co_map(self, loai, so_man):
        if loai == 'me_cung':
            return lay_map_me_cung(so_man) is not None
        return lay_map_pve(so_man) is not None

    def update(self):
        self._tao_font()
        if self._lop == _LOP_CHOI:
            self._game.update()

    # ── Vẽ ────────────────────────────────────────────────
    def ve(self):
        if self._lop == _LOP_CHOI:
            self._game.ve(); return

        w, h = self.man_hinh.get_size()
        self._tao_font()
        ve_nen_chung(self.man_hinh)

        if self._lop == _LOP_CHON_LOAI:
            self._ve_chon_loai(w, h)
        elif self._lop == _LOP_CHON_MAN:
            self._ve_chon_man(w, h)
        elif self._lop == _LOP_SAP_RA:
            self._ve_chon_man(w, h)
            self._ve_sap_ra(w, h)

    def _ve_chon_loai(self, w, h):
        self._r_loai = []
        tieu = self.ft.render("Trò Chơi Khác", True, VANG)
        ty   = h // 10
        self.man_hinh.blit(tieu, tieu.get_rect(center=(w//2, ty)))
        pygame.draw.line(self.man_hinh, (60,60,120),
                         (w//2-220, ty+28), (w//2+220, ty+28), 1)

        NW = int(w*0.32); NH = int(h*0.38)
        gap = int(w*0.06)
        x0  = (w - NW*2 - gap) // 2
        cy  = h//2 + 20
        mx, my = pygame.mouse.get_pos()

        DATA = [
            ('me_cung', 'Mê Cung',  'Góc nhìn tối  •  Tinh linh',  (40,40,120),(80,80,220)),
            ('pve',     'PvE',       'Chiến đấu  •  Toàn map',       (80,20,20), (200,60,60)),
        ]
        for i, (key, ten, mo, mn, mv) in enumerate(DATA):
            x = x0 + i*(NW+gap); y = cy - NH//2
            r = pygame.Rect(x, y, NW, NH)
            self._r_loai.append((r, key))
            hv = r.collidepoint(mx, my)
            pygame.draw.rect(self.man_hinh,
                             tuple(min(c+30,255) for c in mn) if hv else mn,
                             r, border_radius=14)
            pygame.draw.rect(self.man_hinh,
                             mv if hv else tuple(c//2 for c in mv),
                             r, 3, border_radius=14)
            t1 = self.fm.render(ten, True, VANG)
            t2 = self.fn.render(mo,  True, (160,160,200))
            self.man_hinh.blit(t1, t1.get_rect(center=(r.centerx, r.centery-16)))
            self.man_hinh.blit(t2, t2.get_rect(center=(r.centerx, r.centery+16)))

        self._r_back_loai = _ve_nut_back(self.man_hinh, self.fn)

    def _ve_chon_man(self, w, h):
        self._r_man = []
        ten_loai = "Mê Cung" if self._loai == 'me_cung' else "PvE"
        tieu = self.ft.render(f"Trò Chơi Khác  —  {ten_loai}", True, VANG)
        ty   = h // 12
        self.man_hinh.blit(tieu, tieu.get_rect(center=(w//2, ty)))
        pygame.draw.line(self.man_hinh, (60,60,120),
                         (w//2-260, ty+26), (w//2+260, ty+26), 1)

        # Nút quay lại
        self._r_back = pygame.Rect(int(w*0.03), int(h*0.03), 90, 34)
        mx, my = pygame.mouse.get_pos()
        hv_b = self._r_back.collidepoint(mx, my)
        pygame.draw.rect(self.man_hinh,
                         (50,50,100) if hv_b else (30,30,70),
                         self._r_back, border_radius=8)
        pygame.draw.rect(self.man_hinh, (100,100,180), self._r_back, 1, border_radius=8)
        self.man_hinh.blit(
            self.fn.render("◀  Quay lại", True, (180,180,230)),
            self.fn.render("◀  Quay lại", True, (180,180,230)).get_rect(
                center=self._r_back.center))

        COT, HANG = 5, 2
        le_t = w*0.07; le_p = w*0.07; le_tr = h*0.22; le_d = h*0.12
        kh   = w*0.02
        o_c  = (w-le_t-le_p-kh*(COT-1))/COT
        o_r  = (h-le_tr-le_d-kh*(HANG-1))/HANG

        for i in range(10):
            hi = i//COT; ci = i%COT
            x  = int(le_t + ci*(o_c+kh))
            y  = int(le_tr + hi*(o_r+kh))
            r  = pygame.Rect(x, y, int(o_c), int(o_r))
            self._r_man.append(r)
            so_man = i+1
            co     = self._co_map(self._loai, so_man)
            hover  = r.collidepoint(mx, my)
            chon   = (i == self._man_chon)
            if hover: self._man_chon = i

            if co:
                mn = (40,40,85) if (chon or hover) else (28,28,60)
                mv = VANG       if (chon or hover) else (65,65,120)
                dy = 2 if (chon or hover) else 1
                mc = TRANG
            else:
                mn = (30,30,50); mv = (50,50,80); dy = 1; mc = (90,90,110)

            pygame.draw.rect(self.man_hinh, mn, r, border_radius=10)
            pygame.draw.rect(self.man_hinh, mv, r, dy, border_radius=10)
            self.man_hinh.blit(
                self.fm.render(f"Màn {so_man}", True, mc),
                self.fm.render(f"Màn {so_man}", True, mc).get_rect(center=r.center))
            if not co:
                t_k = self.fn.render("Sắp ra", True, (80,80,110))
                self.man_hinh.blit(t_k, t_k.get_rect(
                    center=(r.centerx, r.bottom-int(o_r*0.2))))



    def _ve_sap_ra(self, w, h):
        ov = pygame.Surface((w,h), pygame.SRCALPHA)
        ov.fill((0,0,0,170)); self.man_hinh.blit(ov, (0,0))
        BW = min(420,w-80); BH = 160
        bx = (w-BW)//2; by = h//2-BH//2
        pygame.draw.rect(self.man_hinh, (20,20,50), (bx,by,BW,BH), border_radius=14)
        pygame.draw.rect(self.man_hinh, VANG,        (bx,by,BW,BH), 2, border_radius=14)
        t1 = self.fm.render("🚧  Sẽ có trong tương lai!", True, VANG)
        t2 = self.fn.render(f"Màn {self._man_chon+1} chưa được mở khóa.", True, TRANG)
        t3 = self.fn.render("Nhấn bất kỳ phím để đóng", True, (120,120,160))
        self.man_hinh.blit(t1, t1.get_rect(center=(w//2, by+50)))
        self.man_hinh.blit(t2, t2.get_rect(center=(w//2, by+90)))
        self.man_hinh.blit(t3, t3.get_rect(center=(w//2, by+130)))

    # ── Sự kiện ───────────────────────────────────────────
    def xu_ly_su_kien(self, su_kien):
        # Đang chơi — delegate sang ManChoiKhac
        if self._lop == _LOP_CHOI:
            ket = self._game.xu_ly_su_kien(su_kien)
            if ket == 've_chon_man':
                self._lop = _LOP_CHON_MAN
            return TRANG_THAI_TRO_CHOI_KHAC

        # Thông báo sắp ra
        if self._lop == _LOP_SAP_RA:
            if su_kien.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self._lop = _LOP_CHON_MAN
            return TRANG_THAI_TRO_CHOI_KHAC

        # Chọn loại
        if self._lop == _LOP_CHON_LOAI:
            if su_kien.type == pygame.KEYDOWN and su_kien.key == pygame.K_ESCAPE:
                return TRANG_THAI_MENU
            if su_kien.type == pygame.MOUSEBUTTONDOWN and su_kien.button == 1:
                if hasattr(self,'_r_back_loai') and self._r_back_loai and                         self._r_back_loai.collidepoint(su_kien.pos):
                    return TRANG_THAI_MENU
                for r, key in self._r_loai:
                    if r.collidepoint(su_kien.pos):
                        self._loai     = key
                        self._man_chon = 0
                        self._lop      = _LOP_CHON_MAN
            return TRANG_THAI_TRO_CHOI_KHAC

        # Chọn màn
        if self._lop == _LOP_CHON_MAN:
            if su_kien.type == pygame.KEYDOWN:
                if su_kien.key == pygame.K_ESCAPE:
                    self._lop = _LOP_CHON_LOAI
                    return TRANG_THAI_TRO_CHOI_KHAC
                if su_kien.key == pygame.K_RIGHT: self._man_chon = (self._man_chon+1)%10
                if su_kien.key == pygame.K_LEFT:  self._man_chon = (self._man_chon-1)%10
                if su_kien.key == pygame.K_DOWN:  self._man_chon = (self._man_chon+5)%10
                if su_kien.key == pygame.K_UP:    self._man_chon = (self._man_chon-5)%10
                if su_kien.key == pygame.K_RETURN:
                    return self._bat_dau_man()
            if su_kien.type == pygame.MOUSEBUTTONDOWN and su_kien.button == 1:
                if self._r_back and self._r_back.collidepoint(su_kien.pos):
                    self._lop = _LOP_CHON_LOAI
                    return TRANG_THAI_TRO_CHOI_KHAC
                for i, r in enumerate(self._r_man):
                    if r.collidepoint(su_kien.pos):
                        self._man_chon = i
                        return self._bat_dau_man()
        return TRANG_THAI_TRO_CHOI_KHAC

    def _bat_dau_man(self):
        so_man = self._man_chon + 1
        if self._co_map(self._loai, so_man):
            self._game.tai_man(self._loai, so_man)
            self._lop = _LOP_CHOI
        else:
            self._lop = _LOP_SAP_RA
        return TRANG_THAI_TRO_CHOI_KHAC
