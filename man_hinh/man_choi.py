# man_hinh/man_choi.py
import pygame
import math
from cai_dat import *
from the_gioi.nhan_vat  import NhanVat
from the_gioi.nen_tang  import NenTang, NenTangBoss, KhucGo, ODict, TileCo, TileLa, KhoiTanHinh, SaoMap
from the_gioi.tinh_linh import TinhLinh
from the_gioi.tinh_linh_dieu_khien import TinhLinhDieuKhien
from the_gioi.vat_the   import Kiem, KeDiChuyen, Sach1x1, KhoiDichChuyen, Gai, QuaCau, KhoiNuoc, KiemBay, KiemMua, KiemNem, TiaBan, KiemCamTay
from the_gioi.boss       import Boss5, Boss10
from tien_ich.camera      import Camera
from tien_ich.hud          import HUD
from tien_ich.man_ket_qua  import ManKetQua
from tien_ich.hoi_thoai    import HoiThoai, ThongBao
from man_hinh.thoai_cac_man import THOAI_MAN, THONG_BAO_VAT
from man_hinh.ban_do        import lay_map
from man_hinh.mapMC         import lay_map_me_cung
from man_hinh.mapPE         import lay_map_pve
from man_hinh.boss5_logic   import Boss5LogicMixin
from man_hinh.boss10_logic  import Boss10LogicMixin
from tien_ich.video_intro   import VideoIntro
from the_gioi.hieu_ung      import QuanLyHieuUng

T = TILE_SIZE


# ══════════════════════════════════════════════════════════
#  Sao trên map
# ══════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════
#  MÀN CHƠI  (kế thừa 2 mixin boss)
# ══════════════════════════════════════════════════════════
class ManChoi(Boss5LogicMixin, Boss10LogicMixin):
    def __init__(self, man_hinh):
        self.man_hinh = man_hinh; self.so_man = 1
        self.tam_dung = False; self.muc_pause = 0
        self.da_thang = False
        self.video       = VideoIntro()
        self.tinh_linh   = TinhLinh()
        self.hud         = HUD()
        self.ket_qua     = ManKetQua()
        self.hoi_thoai   = HoiThoai()
        self.thong_bao   = ThongBao()
        self.hieu_ung   = QuanLyHieuUng()
        self.co_kiem     = False
        self.co_hoan_doi = False
        self._kiem_cam   = KiemCamTay()
        self.da_co_dash  = False
        self._giap_cd     = 0
        self.GIAP_CD      = 5 * FPS   # 5 giây hồi chiêu Q
        self._ds_cau          = pygame.sprite.Group()
        self._i_frames        = 0
        self.hieu_ung   = QuanLyHieuUng()
        self._dang_la_tinh_linh = False
        self._tl_dieu_khien   = None
        self._nhan_vat_goc_pos = (0, 0)
        self._man9_tl         = None
        self._tao_font()
        self._tai_ban_do()

    def _tao_font(self):
        w, h = self.man_hinh.get_size()
        self.ft = pygame.font.SysFont(FONT_CHINH, max(30, h//12), bold=True)
        self.fm = pygame.font.SysFont(FONT_CHINH, max(18, h//24), bold=True)
        self.fn = pygame.font.SysFont(FONT_CHINH, max(13, h//36))

    def tai_man(self, n):
        self.so_man = n; self.da_thang = False; self.tam_dung = False
        self.tinh_linh = TinhLinh()
        self.hud.reset()
        self.ket_qua.an()
        self.hoi_thoai = HoiThoai()
        self.thong_bao = ThongBao()
        if self.so_man in THOAI_MAN and self.so_man != 1:
            self.hoi_thoai.bat_dau(THOAI_MAN[self.so_man])
        self.co_hoan_doi = (n >= 4) and (n not in (6, 7, 8, 9))
        self.hieu_ung   = QuanLyHieuUng()
        self._dang_la_tinh_linh = False
        self._tl_dieu_khien = None
        self._boss_win  = False
        self._boss_timer = 0
        self._tai_ban_do()
        # PHẢI set sau _tai_ban_do() vì NhanVat tạo lại ở đó
        if self.so_man >= 3:
            self.nhan_vat.co_danh = True
        self.nhan_vat.co_bay = self.so_man >= 6
        if n >= 4:   self.nhan_vat.co_dash = True;  self.da_co_dash = True
        elif n == 3: self.nhan_vat.co_dash = self.da_co_dash
        else:        self.nhan_vat.co_dash = False
        if n == 1: self.video.bat()

    def tai_man_khac(self, loai, so_man):
        """Load màn từ TroChoiKhac — mapMC hoặc mapPE."""
        if loai == 'me_cung':
            ban_do = lay_map_me_cung(so_man)
            la_boss = False
        else:
            ban_do = lay_map_pve(so_man)
            la_boss = False

        if ban_do is None:
            return False   # không có map

        # Dùng _tai_ban_do nhưng override map
        self._map_override = (ban_do, la_boss)
        self.so_man    = so_man
        self.da_thang  = False
        self.tam_dung  = False
        self.tinh_linh = TinhLinh()
        self.hud.reset()
        self.ket_qua.an()
        self.hoi_thoai = HoiThoai()
        self.thong_bao = ThongBao()
        self.hieu_ung   = QuanLyHieuUng()
        self._dang_la_tinh_linh = False
        self._tl_dieu_khien     = None
        self._boss_win  = False
        self._boss_timer = 0
        # Màn mê cung → giống màn 9 (tinh linh điều khiển, zoom full)
        # Màn pve      → giống màn 5/10 (zoom boss)
        self._tai_ban_do()
        return True

    def _tai_ban_do(self):

        if hasattr(self, '_map_override') and self._map_override:
            ban_do, la_boss      = self._map_override
            self._map_override   = None
        else:
            ban_do, la_boss = lay_map(self.so_man)
        self.ban_do = ban_do; self.la_boss = la_boss
        Tile = NenTangBoss if la_boss else NenTang
        self.ds_nen       = pygame.sprite.Group()
        self.ds_vat       = pygame.sprite.Group()
        self.ds_dich      = pygame.sprite.Group()
        self.ds_kiem      = pygame.sprite.Group()
        self.ds_ke        = pygame.sprite.Group()
        self.ds_sach      = pygame.sprite.Group()
        self.ds_dc        = pygame.sprite.Group()
        self.ds_sao_map   = pygame.sprite.Group()
        self.ds_roi       = pygame.sprite.Group()
        self.ds_boss      = pygame.sprite.Group()
        self._ds_cau      = pygame.sprite.Group()
        self.ds_nuoc      = pygame.sprite.Group()
        self._ds_kiem_nem = pygame.sprite.Group()
        self._ds_kiem_bay = pygame.sprite.Group()
        self._ds_kiem_mua = pygame.sprite.Group()
        self.ds_la        = pygame.sprite.Group()   # lá trang trí trên tile C
        self._i_frames    = 0
        self._boss_timer  = 0
        self._boss_win    = False
        sx = sy = 0
        map_w_tile = len(ban_do[0]) if ban_do else 40
        for ri, hang in enumerate(ban_do):
            for ci, o in enumerate(hang):
                if   o == '#': self.ds_nen.add(Tile(ci, ri))
                elif o == 'T': self.ds_nen.add(KhoiTanHinh(ci, ri))
                elif o == 'C': self.ds_nen.add(TileCo(ci, ri))
                elif o == 'W': self.ds_vat.add(KhucGo(ci, ri))
                elif o == 'K': self.ds_kiem.add(Kiem(ci, ri, ngang=False))
                elif o == 'S': self.ds_sach.add(Sach1x1(ci, ri))
                elif o == '~': self.ds_nuoc.add(KhoiNuoc(ci, ri))
                elif o == 'A' and ri == 5 and ci == 25: self.ds_dc.add(KhoiDichChuyen(ci, ri, 55, 5)) 
                elif o == 'Z' and ri == 5 and ci == 55: self.ds_dc.add(KhoiDichChuyen(ci, ri, 25, 5)) 
                elif o == 'B' and ri == 5 and ci == 89: self.ds_dc.add(KhoiDichChuyen(ci, ri, 128, 0)) 
                elif o == 'D' and ri == 0 and ci == 128: self.ds_dc.add(KhoiDichChuyen(ci, ri, 89, 5))

                elif o == '5':   # spawn Boss5
                    bx5, by5 = ci, ri
                    self.ds_boss.add(Boss5(bx5, by5))
                elif o == '1':   # spawn Boss10
                    bx10, by10 = ci, ri
                    self.ds_boss.add(Boss10(bx10, by10))
                elif o == 'E':
                    co_tc = self.so_man in (5, 6, 7, 8, 9, 10)
                    bien_t = max(1, ci - 15)
                    bien_p2 = min(map_w_tile - 1, ci + 15)
                    ke = KeDiChuyen(ci, ri, bien_t, bien_p2,
                                    co_tan_cong=co_tc, so_man=self.so_man)
                    if self.so_man in (5, 10):
                        ke.mau = 3
                    self.ds_ke.add(ke)
                elif o == '$': self.ds_sao_map.add(SaoMap(ci, ri))
                elif o == 'R': self.ds_roi.add(Gai(ci, ri))
                elif o == 'P': sx, sy = ci, ri
                elif o == '*': self.ds_dich.add(ODict(ci, ri))

        # ── Spawn lá trang trí: tile C mà hàng trên là khoảng trống ──
        KHOI_DUNG = ('#', 'C', '~', 'W')   # ký hiệu không cho lá mọc xuyên
        for ri, hang in enumerate(ban_do):
            for ci, o in enumerate(hang):
                if o == 'C' and not self.la_boss:
                    o_tren = ban_do[ri-1][ci] if ri > 0 else ' '
                    if o_tren not in KHOI_DUNG:
                        self.ds_la.add(TileLa(ci, ri))

        # Màn 9: không tạo nhân vật thật, chỉ dùng tinh linh điều khiển
        if self.so_man == 9:
            # Tạo nhân vật giả ngoài màn để tránh crash các hàm cần nhan_vat
            self.nhan_vat  = NhanVat(-9999, -9999)
            self.nhan_vat.khoa(True)
            self.spawn_pos = (-9999, -9999)
        else:
            self.nhan_vat = NhanVat(sx*T, sy*T)
            self.nhan_vat.so_kiem = 0
            self.spawn_pos = (sx*T, sy*T)

        # Boss được spawn từ ký hiệu '5'/'1' trong map ở vòng for phía trên

        # Vars skill boss (reset mỗi lần tải màn boss)
        if self.so_man in (5, 10):
            self._bsk_sk1_next   = 5 * FPS
            self._ds_tia_ban     = pygame.sprite.Group()
            self._bsk_sk2_done   = False
            self._bsk_sk2_active = False
            self._bsk_sk2_timer  = 0
            self._bsk_khoi_an    = []
            self._bsk_ke_an      = []

        if self.so_man == 10:
            self._b10_phase      = 1
            self._b10_hp         = 10
            self._b10_sk1_count  = 0
            self._b10_sk1_next   = 5 * FPS
            self._b10_sk2_phase  = False
            self._b10_sk3_queue  = 0
            self._b10_sk3_timer  = 0
            self._b10_sk3_count  = 0
            self._b10_teleported = False
            self._b10_sk4_active = False
            self._b10_sk4_dem    = 0
            self._b10_sk4_sokem  = 0
            self._b10_sk4_spawned= 0
            self._b10_sk4_da_tha    = False
            self._b10_sk4_kiem_treo = []
            self._b10_bd_active  = True
            self._b10_bd_cd      = 0
            self._b10_bd_ne      = 0
            self._b10_bd_ne_dir  = 1
            self._b10_enrage        = False   # True khi HP <=5 (phase2) — chỉ SK3/SK4
            self._b10_tuyet_vong_cd = 0       # cooldown SK3 khi <=5HP (3 giây)
            self._b10_dash_hit      = False
            self._b10_f_hit         = False   # F đánh trúng boss frame này

        rong = len(ban_do[0]) * T; cao = len(ban_do) * T
        self.camera = Camera(rong, cao)

        if self.so_man == 1:
            self.tinh_linh.bat_dau(sx*T + T*3, sy*T)
        elif self.so_man == 2:
            self.tinh_linh.bat_dau(sx*T + T*2, sy*T)
        elif self.so_man == 3:
            self.tinh_linh.bat_dau(sx*T + T*2, sy*T)
        elif self.so_man == 4:
            self.tinh_linh.bat_dau(sx*T + T*2, sy*T)
            self.co_hoan_doi = True
        elif self.so_man == 5:
            # Spawn sát bên phải nhân vật
            self.tinh_linh.bat_dau(sx*T + T, sy*T)
        elif self.so_man == 10:
            # Spawn sát bên phải nhân vật
            self.tinh_linh.bat_dau(sx*T + T, sy*T)

        if self.so_man == 9:
            self._man9_tl = TinhLinhDieuKhien(sx*T, sy*T)
            # Không khóa gì thêm — nhan_vat giả đã ở ngoài màn
        else:
            self._man9_tl = None

    def _hoi_sinh(self):
        self.nhan_vat.rect.topleft = self.spawn_pos
        self.nhan_vat.vel_y = self.nhan_vat.vel_x = 0

    def _tinh_linh_noi(self, cau):
        """Kích hoạt tinh linh nói một câu thoại ngắn nếu đang hiện."""
        if self.tinh_linh.hien:
            self.tinh_linh.cau_thoai = cau
            self.tinh_linh.kich_hoat_thoai()

    def _kiem_tra_cham_T(self):
        """Kiểm tra nhân vật vừa bị chặn bởi khối T → tinh linh nói."""
        if not self.tinh_linh.hien: return
        for n in self.ds_nen:
            if not isinstance(n, KhoiTanHinh): continue
            if self.nhan_vat.rect.colliderect(n.rect):
                if not self.tinh_linh.dang_noi:
                    if self.so_man in (5, 10):
                        self._tinh_linh_noi("Can than te!")
                    else:
                        self._tinh_linh_noi("Hinh nhu duong nay khong di duoc...")
                return

    def _mat_mang(self):
        """Trừ 1 máu khi bị đánh. Ở màn 5/10, Q tự động bảo vệ:
        - Đang bất tử → không trừ máu.
        - Q đã hồi (chưa active) → tự bật Q ngay (3s), KHÔNG trừ máu đòn này,
          ĐẶT cooldown Q (_giap_cd = GIAP_CD = 5s).
        - Q đang hồi (cooldown) và không bất tử → trừ máu thật; nếu còn sống
          thì bật bất tử 3s để chống combo, KHÔNG ảnh hưởng cooldown Q.
        Các màn khác: trừ máu bình thường, không có Q.
        Trả về True nếu game over (hết máu)."""
        if self.so_man in (5, 10):
            if self.hieu_ung.dang_bat_tu:
                return False

            if self._giap_cd <= 0:
                # Q đã hồi → tự động bật ngay, đỡ đòn này hoàn toàn
                self.hieu_ung.kich_hoat('bat_tu')
                self._giap_cd = self.GIAP_CD
                return False

        go = self.hud.mat_mang()
        if not go and self.so_man in (5, 10):
            # Bất tử do mất máu (chống combo) — KHÔNG ảnh hưởng cooldown Q
            self.hieu_ung.kich_hoat('bat_tu')
        return go

    def _so_sao_thang(self):
        """Số sao hiển thị khi thắng màn.
        Màn 5/10 (boss): tính theo số mạng còn lại (không nhặt sao trên map).
        Các màn khác: theo số sao đã nhặt trên map."""
        if self.so_man in (5, 10):
            return self.hud.sao_theo_mang()
        return self.hud.sao

    def _teleport(self, dest_x, dest_y):
        self.nhan_vat.rect.topleft = (dest_x, dest_y)
        self.nhan_vat.vel_y = 0; self.nhan_vat.vel_x = 0
        if self.tinh_linh.hien:
            self.tinh_linh.x = float(dest_x + TILE_SIZE)
            self.tinh_linh.y = float(dest_y)
            self.tinh_linh._dang_di_chuyen = False
            self.tinh_linh.la_platform     = False

    # ══════════════════════════════════════════════════════
    #  UPDATE
    # ══════════════════════════════════════════════════════
    def update(self):
        self._tao_font()
        if self.tam_dung: return
        if self.ket_qua.hien: return

        # Thoại màn 1 sau video
        if (self.so_man == 1 and not self.video.hien
                and not self.hoi_thoai.dang_hien
                and not self.hoi_thoai._cac_dong
                and 1 in THOAI_MAN):
            self.hoi_thoai.bat_dau(THOAI_MAN[1])

        self.hoi_thoai.update()
        self.thong_bao.update()

        # Camera luôn cập nhật kể cả khi đang thoại — tránh nhân vật bị vẽ lệch
        if self.so_man in (5, 10) or self.so_man == 9:
            _w, _h = self.man_hinh.get_size()
            self.camera.cap_nhat_boss(_w, _h)
        elif not (self._dang_la_tinh_linh and self._tl_dieu_khien):
            self.camera.cap_nhat(self.nhan_vat)

        if self.hoi_thoai.dang_hien or self.thong_bao.dang_hien:
            return

        self.nhan_vat.khoa(self.video.hien or self._dang_la_tinh_linh)

        # Giáp bất tử — chỉ giữ cooldown
        if self._giap_cd > 0: self._giap_cd -= 1

        # Tinh linh điều khiển
        if self._dang_la_tinh_linh and self._tl_dieu_khien:
            self._tl_dieu_khien.update(list(self.ds_nen) + list(self.ds_vat))

        # Danh sách va chạm
        tat_ca = list(self.ds_nen) + list(self.ds_vat)
        if self.tinh_linh.hien and self.tinh_linh.la_platform:
            tl_rect = self.tinh_linh.rect
            if tl_rect:
                class _P:
                    def __init__(self, r): self.rect = r
                tat_ca.append(_P(tl_rect))

        co_thoai_mo = any(dc._cho_tra_loi for dc in self.ds_dc)
        chuot_giu = pygame.mouse.get_pressed()[0] and not self.video.hien and not co_thoai_mo

        # Màn 9: chỉ tinh linh — bỏ qua toàn bộ logic nhân vật
        if self.so_man == 9:
            if self._man9_tl:
                self._man9_tl.update(list(self.ds_nen))
                # Nhặt sao
                for s in list(self.ds_sao_map):
                    if self._man9_tl.rect.colliderect(s.rect):
                        self.ds_sao_map.remove(s)
                        self.hud.nhat_sao()
                # Tới đích
                for d in self.ds_dich:
                    if self._man9_tl.rect.colliderect(d.rect):
                        self.da_thang = True
                        self.ket_qua.hien_thang(self.so_man, self._so_sao_thang())
                        break
            # Camera cố định
            _w, _h = self.man_hinh.get_size()
            self.camera.cap_nhat_boss(_w, _h)
            self.ds_sao_map.update()
            self.ds_la.update()
            return

        self.nhan_vat.kiem_tra_co_the_leo(tat_ca)
        self.nhan_vat.trong_nuoc = any(
            self.nhan_vat.rect.colliderect(n.rect) for n in self.ds_nuoc)
        self.nhan_vat.update(tat_ca, chuot_trai_giu=chuot_giu)
        self.ds_nuoc.update()
        self.hieu_ung.update(self.nhan_vat)

        # Đánh F
        if self.so_man == 10:
            self._b10_f_hit = False   # reset mỗi frame, set lại nếu F trúng boss
        if self.nhan_vat._danh_signal:
            # Nếu đang bị đóng băng → F dùng để phá băng, không đánh quái
            if self.hieu_ung.dang_bi_dong_bang:
                self.hieu_ung.dong_bang.nhan_danh(self.nhan_vat)
            else:
                T2 = T
                if self.nhan_vat.huong == 1:
                    hit = pygame.Rect(self.nhan_vat.rect.right, self.nhan_vat.rect.top,
                                      T2, self.nhan_vat.rect.height)
                else:
                    hit = pygame.Rect(self.nhan_vat.rect.left - T2, self.nhan_vat.rect.top,
                                      T2, self.nhan_vat.rect.height)
                # Hiệu ứng vệt chém 2x2 đè lên vùng đánh
                self.hieu_ung.tan_cong.kich_hoat(self.nhan_vat.rect, self.nhan_vat.huong)
                for ke in list(self.ds_ke):
                    if hit.colliderect(ke.rect) and not ke._bien_mat:
                        ke.nhan_don(); break
                # F đánh trúng boss10 → trừ 1 máu + kích hoạt bị động
                if self.so_man == 10:
                    for b in list(self.ds_boss):
                        if hit.colliderect(b.rect) and hasattr(b, 'nhan_don'):
                            b.nhan_don()
                            self._b10_f_hit = True
                            break

        # Kiếm mưa boss10: không thể nhặt (theo thiết kế mới)

        # Ném kiếm
        self._ds_kiem_nem.update(list(self.ds_nen) + list(self.ds_vat))
        if self.nhan_vat._nem_signal:
            cx = self.nhan_vat.rect.centerx
            cy = self.nhan_vat.rect.centery
            self._ds_kiem_nem.add(KiemNem(cx, cy, self.nhan_vat.huong))

        for kn in list(self._ds_kiem_nem):
            for b in list(self.ds_boss):
                if kn.cham_boss(b.rect):
                    kn.kill()
                    if hasattr(b, 'nhan_don'): b.nhan_don()
                    break

        self.tinh_linh.update(self.nhan_vat.rect, list(self.ds_nen) + list(self.ds_vat))
        self._kiem_tra_cham_T()

        # Camera
        if self.so_man in (5, 9, 10):
            _w, _h = self.man_hinh.get_size()
            self.camera.cap_nhat_boss(_w, _h)
        elif self._dang_la_tinh_linh and self._tl_dieu_khien:
            self.camera.cap_nhat_vi_tri(
                self._tl_dieu_khien.rect.centerx,
                self._tl_dieu_khien.rect.centery)
        else:
            self.camera.cap_nhat(self.nhan_vat)

        self.ds_kiem.update()
        for ke in self.ds_ke:
            ke.update(list(self.ds_nen), player_rect=self.nhan_vat.rect)

        # Quái tấn công player
        if self._i_frames <= 0:
            for ke in list(self.ds_ke):
                hit, dx, dy = ke.kiem_tra_tan_cong(self.nhan_vat.rect, self._i_frames)
                if hit:
                    if 1 <= self.so_man <= 4:
                        self.nhan_vat.vel_y = -9
                        self._i_frames = KeDiChuyen.I_FRAMES
                        self.so_frame_day = 8
                        self.huong_day_lui = dx
                    elif 6 <= self.so_man <= 9:
                        go = self._mat_mang()
                        if go: self.ket_qua.hien_thua(self.so_man)
                        else:
                            self.nhan_vat.vel_y = -9
                            self._i_frames = KeDiChuyen.I_FRAMES
                            self.so_frame_day = 8
                            self.huong_day_lui = dx
                    break

        if 6 <= self.so_man <= 9 and self._i_frames <= 0:
            for ke in list(self.ds_ke):
                if ke._dan is not None and ke._dan.cham_nguoi(self.nhan_vat.rect):
                    dan = ke._dan
                    if hasattr(dan, '_vx'):
                        huong_day = 1 if dan._vx >= 0 else -1
                    else:
                        huong_day = 1 if ke.rect.centerx < self.nhan_vat.rect.centerx else -1
                    # Tắt đạn
                    if hasattr(dan, '_con_song'):
                        dan._con_song = False
                    elif hasattr(dan, '_alive'):
                        dan._alive = False
                    else:
                        dan.kill()
                    ke._dan = None
                    go = self._mat_mang()
                    if go:
                        self.ket_qua.hien_thua(self.so_man)
                    else:
                        self._i_frames = KeDiChuyen.I_FRAMES
                        self.nhan_vat.vel_x  = huong_day * KeDiChuyen.LUC_DAY
                        self.nhan_vat.vel_y  = -6
                        self.so_frame_day    = 10
                        self.huong_day_lui   = huong_day
                    break

        if hasattr(self, 'so_frame_day') and self.so_frame_day > 0:
            self.so_frame_day -= 1
            self.nhan_vat.rect.x += self.huong_day_lui * 1

        if self._i_frames > 0: self._i_frames -= 1

        nen_vat = list(self.ds_nen) + list(self.ds_vat)
        # Đạn không va chạm với KhoiTanHinh (khối tàng hình)
        from the_gioi.nen_tang import KhoiTanHinh
        nen_vat_dac = [n for n in nen_vat if not isinstance(n, KhoiTanHinh)]
        for c in self._ds_cau: c.update(nen_vat_dac)
        self.ds_sach.update()
        self.ds_dc.update()
        for dc in self.ds_dc:
            dc.xu_ly_vung(self.nhan_vat.rect)
        self.ds_boss.update()
        self.ds_sao_map.update()
        self.ds_la.update()

        # ── Gọi logic boss ────────────────────────────────
        if self.so_man == 5:
            self._update_boss5()
        elif self.so_man == 10:
            self._update_boss10()

        # Tinh linh nhặt sao
        if self._dang_la_tinh_linh and self._tl_dieu_khien:
            nhat_tl = pygame.sprite.spritecollide(
                type('_R', (), {'rect': self._tl_dieu_khien.rect})(),
                self.ds_sao_map, True)
            for _ in nhat_tl: self.hud.nhat_sao()

        self.ds_roi.update(list(self.ds_nen) + list(self.ds_vat))
        if self._i_frames <= 0:
            for gai in list(self.ds_roi):
                if gai.kiem_tra_cham_nguoi(self.nhan_vat.rect):
                    go = self._mat_mang()
                    self._hoi_sinh()
                    if go: self.ket_qua.hien_thua(self.so_man)
                    else:  self._i_frames = KeDiChuyen.I_FRAMES
                    break

        nhat = pygame.sprite.spritecollide(self.nhan_vat, self.ds_sao_map, True)
        for _ in nhat: self.hud.nhat_sao()

        # Rơi xuống đáy
        if self.nhan_vat.rect.top > len(self.ban_do)*T + 50:
            if self.so_man in (5, 10):
                self._boss_hien_khoi()
                go = self._mat_mang()
                if go: self.ket_qua.hien_thua(self.so_man)
                else:
                    self._hoi_sinh()
                    self._i_frames = 5 * FPS
            else:
                game_over = self._mat_mang()
                if game_over: self.ket_qua.hien_thua(self.so_man)
                else: self._hoi_sinh()

        if pygame.sprite.spritecollide(self.nhan_vat, self.ds_dich, False):
            self.da_thang = True
            self.ket_qua.hien_thang(self.so_man, self._so_sao_thang())

    # ══════════════════════════════════════════════════════
    #  VẼ
    # ══════════════════════════════════════════════════════
    def ve(self):
        w, h = self.man_hinh.get_size()
        cam  = self.camera

        # ── Màn boss và màn 9: vẽ vào canvas kích thước map → scale zoom out
        if self.la_boss or self.so_man == 9:
            map_w  = int(self.camera.rong_the_gioi)
            map_h  = int(self.camera.cao_the_gioi)
            canvas = pygame.Surface((map_w, map_h))
            if self.so_man == 9:
                canvas.fill((0, 0, 0))
            else:
                canvas.fill((35, 15, 15))
            # Vẽ tile + vật thể lên canvas
            for s in [*self.ds_nen, *self.ds_dich, *self.ds_vat, *self.ds_kiem,
                      *self.ds_ke, *self.ds_sach, *self.ds_dc, *self.ds_roi]:
                canvas.blit(s.image, s.rect)
            if self.so_man == 9:
                # Màn 9: sao + tinh linh + bóng tối
                for s in self.ds_sao_map:
                    canvas.blit(s.image, s.rect)
                if self._man9_tl:
                    self._man9_tl.ve(canvas, 0, 0)
                    # Bóng tối tâm = vị trí tinh linh trên canvas
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
                # Scale + HUD đơn giản
                ty_le  = cam.ty_le
                sw     = int(map_w * ty_le); sh = int(map_h * ty_le)
                scaled = pygame.transform.scale(canvas, (sw, sh))
                ox = (w - sw) // 2; oy = (h - sh) // 2
                self.man_hinh.fill((0, 0, 0))
                self.man_hinh.blit(scaled, (max(0,ox), max(0,oy)))
                self.hud.ve_don_gian(self.man_hinh)
                self._ve_nut(w)
                self.ket_qua.ve(self.man_hinh)
                self.hoi_thoai.ve(self.man_hinh)
                self.thong_bao.ve(self.man_hinh)
                if self.tam_dung: self._ve_pause(w, h)
                return
            else:
                self._ve_canvas_boss(canvas, cam, w, h)
                return

        # ── Chế độ bình thường ────────────────────────────
        if self.so_man == 9:
            self.man_hinh.fill((0, 0, 0))
        elif self.la_boss:
            self.man_hinh.fill((35, 15, 15))
        else:
            self.man_hinh.fill((90, 165, 245))
        for s in [*self.ds_nen, *self.ds_dich, *self.ds_vat, *self.ds_kiem,
                  *self.ds_ke, *self.ds_sach, *self.ds_dc, *self.ds_roi]:
            self.man_hinh.blit(s.image, cam.ap_dung(s))

        for ke in self.ds_ke:
            if ke._dan is not None:
                dan_alive = ke._dan.con_song() if hasattr(ke._dan, 'con_song') \
                            else (ke._dan.alive() if not hasattr(ke._dan, '_alive') else ke._dan._alive)
                if dan_alive:
                    dr = ke._dan.rect.move(-cam.lech_x, -cam.lech_y)
                    self.man_hinh.blit(ke._dan.image, dr)

        for n in self.ds_nuoc:
            self.man_hinh.blit(n.image, cam.ap_dung(n))
        # Lá trang trí — vẽ sau đất, trước nhân vật
        for la in self.ds_la:
            self.man_hinh.blit(la.image, cam.ap_dung(la))
        self.man_hinh.blit(self.nhan_vat.image, cam.ap_dung(self.nhan_vat))
        # Kiếm cầm tay (ẩn khi di chuyển/leo/đánh)
        self._kiem_cam.ve(self.man_hinh, cam.lech_x, cam.lech_y,
                          self.nhan_vat, self.hieu_ung)
        # Hiệu ứng xấu — vẽ ngay sau nhân vật
        self.hieu_ung.ve(self.man_hinh, cam.lech_x, cam.lech_y, self.nhan_vat)



        if self._dang_la_tinh_linh and self._tl_dieu_khien:
            self._tl_dieu_khien.ve(self.man_hinh, cam.lech_x, cam.lech_y)

        for s in self.ds_sach:
            if s.gan_nguoi_choi(self.nhan_vat.rect) and not s._bien_mat:
                s.ve_hint(self.man_hinh, cam.lech_x, cam.lech_y, self.fn)
        for dc in self.ds_dc:
            dc.ve_hoi_thoai(self.man_hinh, cam.lech_x, cam.lech_y, w, h)
        for k in self.ds_kiem:
            if k.gan_nguoi_choi(self.nhan_vat.rect) and not k._bien_mat:
                k.ve_hint(self.man_hinh, cam.lech_x, cam.lech_y, self.fn)

        for c in self._ds_cau:
            self.man_hinh.blit(c.image, cam.ap_dung(c))
        if self.so_man == 5 and hasattr(self, '_ds_tia_ban'):
            for tia in self._ds_tia_ban:
                self.man_hinh.blit(tia.image, cam.ap_dung(tia))
        if self.so_man == 10:
            for k in self._ds_kiem_bay:
                self.man_hinh.blit(k.image, cam.ap_dung(k))
            for k in self._ds_kiem_mua:
                self.man_hinh.blit(k.image, cam.ap_dung(k))
        for kn in self._ds_kiem_nem:
            self.man_hinh.blit(kn.image, cam.ap_dung(kn))
        for b in self.ds_boss:
            self.man_hinh.blit(b.image, cam.ap_dung(b))

        if self.so_man == 5:
            for b in self.ds_boss:
                con_lai = max(0, (60*FPS - self._boss_timer)/FPS)
                b.ve_thanh_thoi_gian(self.man_hinh, cam.lech_x, cam.lech_y, con_lai, self.fn)
        elif self.so_man == 10:
            for b in self.ds_boss:
                b.ve_thanh_mau(self.man_hinh, cam.lech_x, cam.lech_y, self.fn)

        for s in self.ds_sao_map:
            self.man_hinh.blit(s.image, cam.ap_dung(s))

        self._ve_nut(w)
        if not self._dang_la_tinh_linh:
            self.tinh_linh.ve(self.man_hinh, cam.lech_x, cam.lech_y, w, h)
        self.video.ve(self.man_hinh)
        self.hud.ve(self.man_hinh, self.nhan_vat, self)

        if self.so_man == 5 and hasattr(self, '_boss_timer'):
            con_lai = max(0, (60*FPS - self._boss_timer)/FPS)
            self._ve_timer_giua(con_lai, 60, w)
        elif self.so_man == 10 and hasattr(self, '_boss_timer'):
            con_lai = max(0, (120*FPS - self._boss_timer)/FPS)
            self._ve_timer_giua(con_lai, 120, w)

        if self.so_man in (5, 10) and getattr(self, '_bsk_sk2_active', False):
            sec = max(0, self._bsk_sk2_timer // FPS)
            a   = int(200 + 55*abs(math.sin(self._bsk_sk2_timer*0.1)))
            fn  = pygame.font.SysFont(FONT_CHINH, 18, bold=True)
            t   = fn.render(f"Khối biến mất! ({sec}s)", True, (255,80,80))
            t.set_alpha(a)
            self.man_hinh.blit(t, t.get_rect(center=(w//2, h-38)))

        self.ket_qua.ve(self.man_hinh)
        self.hoi_thoai.ve(self.man_hinh)
        self.thong_bao.ve(self.man_hinh)
        if self.tam_dung: self._ve_pause(w, h)

    def _ve_canvas_boss(self, canvas, cam, w, h):
        """Vẽ toàn bộ nội dung boss lên canvas kích thước map,
        rồi scale canvas xuống vừa màn hình (zoom out)."""
        # ── Vẽ nước ──
        for n in self.ds_nuoc:
            canvas.blit(n.image, n.rect)
            
        # ── Lá ──
        for la in self.ds_la:
            canvas.blit(la.image, la.rect)
            
        # ── Nhân vật ──
        canvas.blit(self.nhan_vat.image, self.nhan_vat.rect)
        # Kiếm cầm tay (ẩn khi di chuyển/leo/đánh)
        self._kiem_cam.ve(canvas, 0, 0, self.nhan_vat, self.hieu_ung)
        # Vẽ hiệu ứng trói chân/bất tử... lên canvas trước khi scale
        self.hieu_ung.ve(canvas, 0, 0, self.nhan_vat)

        # ── Quả cầu ──
        for c in self._ds_cau:
            canvas.blit(c.image, c.rect)

        # ── Tia bắn SK3 ──
        if hasattr(self, '_ds_tia_ban'):
            for tia in self._ds_tia_ban:
                canvas.blit(tia.image, tia.rect)
            
        # ── Kiếm bay/mưa/ném ──
        for k in self._ds_kiem_bay:
            canvas.blit(k.image, k.rect)
        for k in self._ds_kiem_mua:
            canvas.blit(k.image, k.rect)
        for kn in self._ds_kiem_nem:
            canvas.blit(kn.image, kn.rect)
            
        # ── Tinh linh ──
        if self.tinh_linh.hien:
            tl_sx = int(self.tinh_linh.x)
            tl_sy = int(self.tinh_linh.y)
            from the_gioi.tinh_linh import _get as _tl_get, S as _TL_S
            canvas.blit(_tl_get(), (tl_sx, tl_sy))
            
        # ── Boss ──
        for b in self.ds_boss:
            canvas.blit(b.image, b.rect)
            
        # ── Sao ──
        for s in self.ds_sao_map:
            canvas.blit(s.image, s.rect)

        # ── Scale canvas → màn hình (letterbox) ──────────
        ty_le   = cam.ty_le
        sw      = int(canvas.get_width()  * ty_le)
        sh      = int(canvas.get_height() * ty_le)
        scaled  = pygame.transform.scale(canvas, (sw, sh))
        
        # Căn giữa màn hình
        ox = (w - sw) // 2
        oy = (h - sh) // 2
        
        # Đổ màu nền tối cho vùng viền ngoài (letterbox)
        self.man_hinh.fill((35, 15, 15))
        self.man_hinh.blit(scaled, (max(0, ox), max(0, oy)))
        
        # ── Vẽ HUD và UI cố định đè lên màn hình chính (Không bị scale nhỏ theo map) ──
        self.hud.ve(self.man_hinh, self.nhan_vat, self)
        self._ve_nut(w)
        
        # Hiển thị thanh máu hoặc thời gian đếm ngược của Boss ở giữa màn hình
        if self.so_man == 5 and hasattr(self, '_boss_timer'):
            con_lai = max(0, (60 * FPS - self._boss_timer) / FPS)
            self._ve_timer_giua(con_lai, 60, w)
        elif self.so_man == 10 and hasattr(self, '_boss_timer'):
            con_lai = max(0, (120 * FPS - self._boss_timer) / FPS)
            self._ve_timer_giua(con_lai, 120, w)
            # Vẽ thanh máu boss10 cố định giữa màn hình
            self._ve_thanh_mau_boss10(w, h)

        # Hiển thị cảnh báo cơ chế Boss (ví dụ: Khối biến mất)
        if getattr(self, '_bsk_sk2_active', False):
            sec = max(0, self._bsk_sk2_timer // FPS)
            a   = int(200 + 55 * math.sin(self._bsk_sk2_timer * 0.1))
            fn  = pygame.font.SysFont(FONT_CHINH, 18, bold=True)
            t   = fn.render(f"⚠ Khối biến mất! ({sec}s)", True, (255, 80, 80))
            t.set_alpha(a)
            self.man_hinh.blit(t, t.get_rect(center=(w // 2, h - 38)))

        # Vẽ các màn hình thông báo hệ thống đè lên cùng
        self.ket_qua.ve(self.man_hinh)
        self.hoi_thoai.ve(self.man_hinh)
        self.thong_bao.ve(self.man_hinh)
        if self.tam_dung:
            self._ve_pause(w, h)

    # ══════════════════════════════════════════════════════
    #  NÚT UI
    # ══════════════════════════════════════════════════════
    NUT_S = 36; NUT_P = 8

    def _ve_nut(self, w):
        s = self.NUT_S; p = self.NUT_P
        # Góc trên PHẢI: pause + mute
        self.r_pause = pygame.Rect(w-s-p, p, s, s)
        self.r_mute  = pygame.Rect(w-2*s-2*p, p, s, s)
        for r in [self.r_pause, self.r_mute]:
            pygame.draw.rect(self.man_hinh, (30,30,30), r, border_radius=8)
            pygame.draw.rect(self.man_hinh, (180,180,180), r, 2, border_radius=8)
        cx, cy = self.r_pause.center
        pygame.draw.rect(self.man_hinh, TRANG, (cx-9, cy-10, 7, 20))
        pygame.draw.rect(self.man_hinh, TRANG, (cx+2,  cy-10, 7, 20))
        cx2, cy2 = self.r_mute.center
        am = getattr(self, 'am_thanh', None)
        am_bat = not (am and am._tat)
        if am_bat:
            pygame.draw.polygon(self.man_hinh, TRANG,
                [(cx2-10,cy2-5),(cx2-2,cy2-5),(cx2+8,cy2-12),(cx2+8,cy2+12),(cx2-2,cy2+5),(cx2-10,cy2+5)])
            pygame.draw.arc(self.man_hinh, TRANG, (cx2+4,cy2-10,12,20), -0.8, 0.8, 2)
        else:
            pygame.draw.polygon(self.man_hinh, XAM,
                [(cx2-10,cy2-5),(cx2-2,cy2-5),(cx2+8,cy2-12),(cx2+8,cy2+12),(cx2-2,cy2+5),(cx2-10,cy2+5)])
            pygame.draw.line(self.man_hinh, DO, (cx2+2,cy2-10), (cx2+14,cy2+10), 3)


    def _ve_thanh_mau_boss10(self, w, h):
        """Vẽ thanh máu boss10 cố định giữa màn hình (phía trên)."""
        b = next(iter(self.ds_boss), None)
        if not b or b.da_chet():
            return
        if not hasattr(self, '_fn_boss_mau'):
            self._fn_boss_mau = pygame.font.SysFont(FONT_CHINH, 16, bold=True)

        BW = min(400, w - 80)
        BH = 16
        bx = w // 2 - BW // 2
        by = 38   # bên dưới timer

        # Nền
        pygame.draw.rect(self.man_hinh, (40, 10, 10), (bx, by, BW, BH), border_radius=6)
        # Thanh máu
        tl = b.mau / b.SO_MAU_MAX
        fw = int(BW * tl)
        if fw > 0:
            pygame.draw.rect(self.man_hinh, (200, 30, 30), (bx, by, fw, BH), border_radius=6)
        # Vạch chia HP
        for i in range(1, b.SO_MAU_MAX):
            vx = bx + int(BW * i / b.SO_MAU_MAX)
            pygame.draw.line(self.man_hinh, (0, 0, 0), (vx, by), (vx, by + BH), 2)
        # Viền
        pygame.draw.rect(self.man_hinh, (220, 150, 150), (bx, by, BW, BH), 1, border_radius=6)
        # Text
        phase_str = f" [Phase {b._phase}]" if hasattr(b, '_phase') else ""
        t = self._fn_boss_mau.render(f"BOSS  {b.mau} / {b.SO_MAU_MAX}{phase_str}", True, TRANG)
        self.man_hinh.blit(t, t.get_rect(center=(w // 2, by - 10)))

    def _ve_timer_giua(self, con_lai, tong, w):
        if not hasattr(self, '_fn_timer'):
            self._fn_timer = pygame.font.SysFont(FONT_CHINH, 22, bold=True)
        mau = (220,80,80) if con_lai < tong*0.2 else VANG
        t = self._fn_timer.render(f"{int(con_lai)}s", True, mau)
        BW = t.get_width()+20; BH = t.get_height()+8
        bx = w//2 - BW//2; by = 8
        ov = pygame.Surface((BW, BH), pygame.SRCALPHA)
        ov.fill((0,0,0,120))
        pygame.draw.rect(ov, mau, (0,0,BW,BH), 2, border_radius=6)
        self.man_hinh.blit(ov, (bx, by))
        self.man_hinh.blit(t, t.get_rect(center=(w//2, by+BH//2)))

    MUC_P = [("Tiếp tục","tc"), ("Chơi lại","cl"), ("Về menu","vm")]

    def _ve_pause(self, w, h):
        ov = pygame.Surface((w, h), pygame.SRCALPHA)
        ov.fill((0,0,0,160)); self.man_hinh.blit(ov, (0,0))
        ti = self.ft.render("Tạm Dừng", True, VANG)
        self.man_hinh.blit(ti, ti.get_rect(center=(w//2, h//2-130)))

        am  = getattr(self, 'am_thanh', None)
        tat = getattr(am, '_tat', False) if am else False
        muc = getattr(am, '_am_luong_nhac', 0.7) if am else 0.7
        if tat: muc = 0.0

        BAR_W=200; BAR_H=8; BAR_X=w//2-BAR_W//2; BAR_Y=h//2-80
        pygame.draw.rect(self.man_hinh, (40,40,70), (BAR_X,BAR_Y,BAR_W,BAR_H), border_radius=4)
        fill_w = int(BAR_W*muc)
        if fill_w > 0:
            pygame.draw.rect(self.man_hinh, (80,180,255), (BAR_X,BAR_Y,fill_w,BAR_H), border_radius=4)
        pygame.draw.rect(self.man_hinh, (80,80,130), (BAR_X,BAR_Y,BAR_W,BAR_H), 1, border_radius=4)
        tx = BAR_X+fill_w; ty = BAR_Y+BAR_H//2
        pygame.draw.circle(self.man_hinh, (150,210,255), (tx,ty), 8)
        pygame.draw.circle(self.man_hinh, (200,230,255), (tx,ty), 8, 2)
        self.r_slider = pygame.Rect(BAR_X, BAR_Y-6, BAR_W, BAR_H+12)
        self._slider_x0 = BAR_X; self._slider_w = BAR_W

        icon = self.fm.render("🔇" if tat else "🔊", True, TRANG)
        self.man_hinh.blit(icon, (BAR_X-30, BAR_Y-8))

        self.r_bat_tat_am = pygame.Rect(BAR_X+BAR_W+10, BAR_Y-6, 54, 20)
        mau_bt = (50,100,50) if not tat else (100,40,40)
        pygame.draw.rect(self.man_hinh, mau_bt, self.r_bat_tat_am, border_radius=5)
        pygame.draw.rect(self.man_hinh,
                         (100,180,100) if not tat else (180,80,80),
                         self.r_bat_tat_am, 1, border_radius=5)
        lbl_bt = self.fn.render("Bật" if tat else "Tắt", True, TRANG)
        self.man_hinh.blit(lbl_bt, lbl_bt.get_rect(center=self.r_bat_tat_am.center))

        self.r_mp = []
        nw = min(320, w-80); nr = max(40, h//14)
        for i, (nhan, _) in enumerate(self.MUC_P):
            y = h//2-30 + i*(nr+10)
            r = pygame.Rect(w//2-nw//2, y, nw, nr)
            self.r_mp.append(r)
            pygame.draw.rect(self.man_hinh,
                             VANG if i==self.muc_pause else (40,40,80), r, border_radius=10)
            pygame.draw.rect(self.man_hinh,
                             CAM  if i==self.muc_pause else (70,70,130), r, 2, border_radius=10)
            chu = self.fm.render(nhan, True, (25,25,25) if i==self.muc_pause else TRANG)
            self.man_hinh.blit(chu, chu.get_rect(center=r.center))

    # ══════════════════════════════════════════════════════
    #  XỬ LÝ SỰ KIỆN
    # ══════════════════════════════════════════════════════
    def xu_ly_su_kien(self, ev):
        if self.video.hien: self.video.xu_ly(ev); return TRANG_THAI_CHOI

        if ev.type == pygame.USEREVENT:
            if ev.dict.get('code') == 'bay_unlock':
                if "bay" in THONG_BAO_VAT:
                    td, nd = THONG_BAO_VAT["bay"]
                    self.thong_bao.hien(nd, tieu_de=td)
                else:
                    self.thong_bao.hien(
                        "Nhan nhay 2 lan de bay! Ton tai 3 giay.",
                        tieu_de="Ky nang moi: Bay")
            return TRANG_THAI_CHOI

        if self.hoi_thoai.dang_hien:
            self.hoi_thoai.xu_ly(ev); return TRANG_THAI_CHOI
        if self.thong_bao.dang_hien:
            self.thong_bao.xu_ly(ev); return TRANG_THAI_CHOI

        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and self.ket_qua.hien:
            w2, h2 = self.man_hinh.get_size()
            ket = self.ket_qua.xu_ly_click(ev.pos, w2, h2)
            if ket == 'choi_lai':
                self.ket_qua.an(); self.tai_man(self.so_man)
            elif ket == 'man_tiep':
                self.ket_qua.an(); self.tai_man(min(10, self.so_man+1))
            elif ket == 'man_chinh':
                self.ket_qua.an(); return TRANG_THAI_MENU
            return TRANG_THAI_CHOI

        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_q and not self.tam_dung:
            if self.so_man in (5, 10):
                if self._giap_cd <= 0 and not self.hieu_ung.dang_bat_tu:
                    self.hieu_ung.kich_hoat('bat_tu')
                    self._giap_cd = self.GIAP_CD
            elif self.co_hoan_doi and self.tinh_linh.hien:
                if not self._dang_la_tinh_linh:
                    self._dang_la_tinh_linh = True
                    self._tl_dieu_khien = TinhLinhDieuKhien(
                        self.tinh_linh.x, self.tinh_linh.y)
                else:
                    self._dang_la_tinh_linh = False
                    if self._tl_dieu_khien:
                        self.tinh_linh.x = self._tl_dieu_khien.x
                        self.tinh_linh.y = self._tl_dieu_khien.y
                    self._tl_dieu_khien = None

        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_f and not self.tam_dung:
            for k in list(self.ds_kiem):
                if k.gan_nguoi_choi(self.nhan_vat.rect) and not k._bien_mat:
                    k.bat_dau_bien_mat(); self.co_kiem = True
                    self.nhan_vat.co_danh = True
                    if "kiem" in THONG_BAO_VAT:
                        td, nd = THONG_BAO_VAT["kiem"]
                        self.thong_bao.hien(nd, tieu_de=td)
            for s in list(self.ds_sach):
                if s.gan_nguoi_choi(self.nhan_vat.rect) and not s._bien_mat:
                    s.bat_dau_bien_mat()
                    self.da_co_dash = True
                    self.nhan_vat.co_dash = True
                    if "sach" in THONG_BAO_VAT:
                        td, nd = THONG_BAO_VAT["sach"]
                        self.thong_bao.hien(nd, tieu_de=td)

        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if not self.tam_dung:
                for dc in self.ds_dc:
                    ket_qua = dc.xu_ly_click_hoi_thoai(ev.pos)
                    if ket_qua == 'co':
                        dest = dc.tra_loi_co(self.nhan_vat.rect)
                        self._teleport(dest[0], dest[1])
                    elif ket_qua == 'khong':
                        dc.tra_loi_khong()
                if self.tinh_linh.hien:
                    cam = self.camera
                    if cam.ty_le < 1.0:
                        # Màn boss/9: có zoom — đổi tọa độ screen → world
                        mw, mh = self.man_hinh.get_size()
                        sw = int(cam.rong_the_gioi * cam.ty_le)
                        sh = int(cam.cao_the_gioi  * cam.ty_le)
                        ox = (mw - sw) // 2
                        oy = (mh - sh) // 2
                        wx = (ev.pos[0] - max(0, ox)) / cam.ty_le
                        wy = (ev.pos[1] - max(0, oy)) / cam.ty_le
                    else:
                        # Bình thường
                        wx = ev.pos[0] + cam.lech_x
                        wy = ev.pos[1] + cam.lech_y
                    self.tinh_linh.xu_ly_click(wx, wy)
            # Nút mute (góc trên phải, bên trái pause)
            if hasattr(self, "r_mute") and self.r_mute.collidepoint(ev.pos):
                am = getattr(self, 'am_thanh', None)
                if am:
                    am.tat_am(not am._tat)
                    if not am._tat:
                        am.choi_nhac(getattr(self, '_nhac_key', 'man_1_4'))
                return TRANG_THAI_CHOI
            # Nút pause (góc trên phải)
            if hasattr(self, "r_pause") and self.r_pause.collidepoint(ev.pos):
                self.tam_dung = not self.tam_dung; self.muc_pause = 0
                return TRANG_THAI_CHOI
            if self.tam_dung:
                am = getattr(self, 'am_thanh', None)
                if hasattr(self, 'r_slider') and self.r_slider.collidepoint(ev.pos):
                    muc = max(0.0, min(1.0, (ev.pos[0]-self._slider_x0)/self._slider_w))
                    if am: am.tang_am(muc); am.tat_am(False)
                    self._dragging_slider = True; return TRANG_THAI_CHOI
                if hasattr(self, 'r_bat_tat_am') and self.r_bat_tat_am.collidepoint(ev.pos):
                    if am:
                        am.tat_am(not am._tat)
                        if not am._tat: am.choi_nhac(getattr(self, '_nhac_key', 'man_1_4'))
                    return TRANG_THAI_CHOI
                if hasattr(self, "r_mp"):
                    for i, r in enumerate(self.r_mp):
                        if r.collidepoint(ev.pos):
                            self.muc_pause = i; return self._do_pause()

        if ev.type == pygame.MOUSEBUTTONUP:
            self._dragging_slider = False

        if ev.type == pygame.MOUSEMOTION:
            if getattr(self, '_dragging_slider', False) and self.tam_dung:
                am = getattr(self, 'am_thanh', None)
                muc = max(0.0, min(1.0, (ev.pos[0]-self._slider_x0)/self._slider_w))
                if am: am.tang_am(muc)
            if self.tam_dung and hasattr(self, "r_mp"):
                for i, r in enumerate(self.r_mp):
                    if r.collidepoint(ev.pos): self.muc_pause = i

        if ev.type == pygame.KEYDOWN:
            if self.tam_dung:
                if ev.key == pygame.K_UP:
                    self.muc_pause = (self.muc_pause-1) % len(self.MUC_P)
                if ev.key == pygame.K_DOWN:
                    self.muc_pause = (self.muc_pause+1) % len(self.MUC_P)
                if ev.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return self._do_pause()
                return TRANG_THAI_CHOI
            if ev.key == pygame.K_ESCAPE:
                self.tam_dung = True; self.muc_pause = 0
            if ev.key == pygame.K_r:
                self.tai_man(self.so_man)

        return TRANG_THAI_CHOI

    def _do_pause(self):
        a = self.MUC_P[self.muc_pause][1]
        if a == "tc": self.tam_dung = False
        elif a == "cl": self.tai_man(self.so_man)
        elif a == "vm": self.tam_dung = False; return TRANG_THAI_MENU
        return TRANG_THAI_CHOI
