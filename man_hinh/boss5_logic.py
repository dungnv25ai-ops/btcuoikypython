                         
import pygame
import math
from cai_dat import *
from the_gioi.vat_the import QuaCau, KeDiChuyen, TiaBan

T = TILE_SIZE

class Boss5LogicMixin:

    def _boss_sk1_ban(self):
        for b in self.ds_boss:
            bx, by = b.rect.centerx, b.rect.centery
            px, py = self.nhan_vat.rect.centerx, self.nhan_vat.rect.centery
            if hasattr(b, 'quay_ve'):
                b.quay_ve(px)
            for ox in (-40, -20, 0, 20, 40):
                self._ds_cau.add(QuaCau(bx + ox, by, px, py))

    def _boss_sk3_thuc_hien(self):

        b = next(iter(self.ds_boss), None)
        if not b:
            return

        px  = self.nhan_vat.rect.centerx
        py  = self.nhan_vat.rect.centery
        KHOANG = 5                   

        map_w = len(self.ban_do[0]) * T

        if hasattr(self.nhan_vat, 'huong'):
            huong = self.nhan_vat.huong
        else:
            huong = 1

        half_w = b.rect.width // 2

        def _thu_vi_tri(huong_dat):

            x_mong_muon = px + huong_dat * (half_w + KHOANG)
            x_clamp     = max(T + half_w, min(x_mong_muon, map_w - T - half_w))
                                                                
            khoang_thuc = abs(x_clamp - px) - half_w
                                 
            test_rect = pygame.Rect(x_clamp - half_w, b.rect.top,
                                    b.rect.width, b.rect.height)
            co_chuong = any(test_rect.colliderect(n.rect) for n in self.ds_nen)
            du_khoang = (khoang_thuc >= KHOANG) and not co_chuong
            return x_clamp, du_khoang

        x_sau, du_sau = _thu_vi_tri(-huong)

        if du_sau:
            dest_x = x_sau
        else:
                                                                  
            x_truoc, _ = _thu_vi_tri(huong)
            dest_x = x_truoc

        b.rect.centerx = dest_x
        b.rect.bottom  = self.nhan_vat.rect.bottom

        if hasattr(b, 'quay_ve'):
            b.quay_ve(px)

        bx = b.rect.centerx
        by = b.rect.centery
        tia = TiaBan(bx, by, px, py)
        self._ds_tia_ban.add(tia)

    def _boss_an_khoi(self, toan_bo_san=False, thoi_gian=None):
        hidden_tiles = list(self.ds_nen)
        for tile in hidden_tiles:
            self.ds_nen.remove(tile)

        hidden_ke = []
        for ke in list(self.ds_ke):
            hidden_ke.append({
                'cot':        ke.rect.x // T,
                'hang':       ke.rect.y // T,
                'co_tan_cong': ke.co_tan_cong,
            })
            ke.kill()

        self._bsk_khoi_an    = hidden_tiles
        self._bsk_ke_an      = hidden_ke
        self._bsk_sk2_active = True
        self._bsk_sk2_timer  = (thoi_gian if thoi_gian is not None else 5 * FPS)

        map_w = len(self.ban_do[0]) * T
        map_h = len(self.ban_do)    * T
        for b in self.ds_boss:
            if hasattr(b, 'khoa_giua_map'):
                b.khoa_giua_map(map_w, map_h)

    def _boss_hien_khoi(self):
        for tile in getattr(self, '_bsk_khoi_an', []):
            self.ds_nen.add(tile)
        self._bsk_khoi_an = []

        for ke_info in getattr(self, '_bsk_ke_an', []):
            ke = KeDiChuyen(
                ke_info['cot'], ke_info['hang'],
                ke_info['cot'] - 10, ke_info['cot'] + 10,
                co_tan_cong=ke_info['co_tan_cong'],
                so_man=self.so_man)
            ke.mau = 3
            self.ds_ke.add(ke)
        self._bsk_ke_an      = []
        self._bsk_sk2_active = False
        self._bsk_sk2_timer  = 0

        for b in self.ds_boss:
            if hasattr(b, 'mo_khoa_vi_tri'):
                b.mo_khoa_vi_tri()

    def _update_boss5(self):
        if not self.ds_boss:
            return

        if self._bsk_sk2_active:
            self._bsk_sk2_timer -= 1
            if self._bsk_sk2_timer <= 0:
                self._boss_hien_khoi()
                                                         
            if hasattr(self, '_ds_tia_ban'):
                self._ds_tia_ban.update()
                if self._i_frames <= 0 and not self.hieu_ung.dang_bat_tu:
                    for tia in list(self._ds_tia_ban):
                        if tia.cham_nguoi(self.nhan_vat.rect):
                            go = self._mat_mang()
                            if go:
                                self._boss_hien_khoi()
                                self.ket_qua.hien_thua(self.so_man)
                            else:
                                self._i_frames = 5 * FPS
                            break
            return                  

        self._boss_timer += 1
        bt = self._boss_timer

        if not hasattr(self, '_ds_tia_ban'):
            self._ds_tia_ban = pygame.sprite.Group()

        if bt in (3*FPS, 13*FPS, 23*FPS, 33*FPS, 43*FPS, 53*FPS):
            if hasattr(self, 'hieu_ung'):
                self.hieu_ung.kich_hoat('troi_chan')

        if bt == 30 * FPS:
            am = getattr(self, 'am_thanh', None)
            if am and getattr(am, '_toc_do_hien', 1.0) == 1.0:
                am.dat_toc_do(1.5)

        if bt == self._bsk_sk1_next:
            self._boss_sk1_ban()
            self._bsk_sk1_next += 10 * FPS

        if bt in (7*FPS, 17*FPS, 37*FPS, 47*FPS, 52*FPS):
            if hasattr(self, 'hieu_ung'):
                self.hieu_ung.kich_hoat('dong_bang')

        if bt in (10*FPS, 20*FPS, 40*FPS, 50*FPS, 55*FPS):
            self._boss_sk3_thuc_hien()

        if bt == 25 * FPS and not self._bsk_sk2_done:
            if not self.nhan_vat.co_bay:
                self.nhan_vat.co_bay = True
                pygame.event.post(pygame.event.Event(
                    pygame.USEREVENT, {'code': 'bay_unlock'}))

        if bt >= 30 * FPS and not self._bsk_sk2_done:
            self._bsk_sk2_done = True
            self._boss_an_khoi(thoi_gian=3 * FPS)

        from the_gioi.nen_tang import KhoiTanHinh
        nen_vat = [n for n in list(self.ds_nen) + list(self.ds_vat)
                   if not isinstance(n, KhoiTanHinh)]
        self._ds_tia_ban.update(nen_vat)

        if (self.so_man == 5
                and self.tinh_linh.hien
                and self._giap_cd <= 0
                and not self.hieu_ung.dang_bat_tu
                and not self.hieu_ung.dang_bi_dong_bang):
            canh_bao = False
            vung = self.nhan_vat.rect.inflate(T * 4, T * 4)
            for c in self._ds_cau:
                if vung.colliderect(c.rect):
                    canh_bao = True; break
            if not canh_bao:
                for tia in self._ds_tia_ban:
                    if vung.colliderect(tia.rect):
                        canh_bao = True; break
            if canh_bao:
                self.hieu_ung.kich_hoat('bat_tu')
                self._giap_cd = self.GIAP_CD

        if self._i_frames <= 0:
            for tia in list(self._ds_tia_ban):
                if tia.cham_nguoi(self.nhan_vat.rect):
                    if self.hieu_ung.dang_bi_dong_bang:
                                                                                           
                        go = self.hud.mat_mang()
                        self.hieu_ung.dong_bang.nhan_danh(self.nhan_vat)
                                                                
                        self.hieu_ung.dong_bang._cap    = self.hieu_ung.dong_bang.SO_LAN_PHA
                        self.hieu_ung.dong_bang._active = False
                        self.hieu_ung.dong_bang.image   = None
                        self.nhan_vat._khoa_dong_bang   = False
                        if go:
                            self._boss_hien_khoi()
                            self.ket_qua.hien_thua(self.so_man)
                        else:
                            self._i_frames = 5 * FPS
                    else:
                        go = self._mat_mang()
                        if go:
                            self._boss_hien_khoi()
                            self.ket_qua.hien_thua(self.so_man)
                        else:
                            self._i_frames = 5 * FPS
                    break

        if self._i_frames <= 0:
            for c in list(self._ds_cau):
                if c.cham_nguoi(self.nhan_vat.rect) and not self.hieu_ung.dang_bat_tu:
                    c.kill()
                    go = self._mat_mang()
                    if go:
                        self._boss_hien_khoi()
                        self.ket_qua.hien_thua(self.so_man)
                    else:
                        self._i_frames = 5 * FPS
                    break

        for b in self.ds_boss:
            if (b.cham_nguoi(self.nhan_vat.rect)
                    and self._i_frames <= 0
                    and not self.hieu_ung.dang_bat_tu):
                go = self._mat_mang()
                if go:
                    self._boss_hien_khoi()
                    self.ket_qua.hien_thua(self.so_man)
                else:
                    self._i_frames = 5 * FPS
                break

        if bt >= 60 * FPS and not self.ket_qua.hien:
            self._boss_hien_khoi()
            self._ds_tia_ban.empty()
            self._boss_win = True
            self.da_thang  = True
            self.ket_qua.hien_thang(self.so_man, self._so_sao_thang())