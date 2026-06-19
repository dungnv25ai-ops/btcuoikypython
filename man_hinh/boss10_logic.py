                          
import pygame
from cai_dat import *
from the_gioi.vat_the import QuaCau, KiemBay, KiemMua

T = TILE_SIZE

class Boss10LogicMixin:

    def _b10_ban_cau(self):
        for b in self.ds_boss:
            bx, by = b.rect.centerx, b.rect.centery
            px, py = self.nhan_vat.rect.centerx, self.nhan_vat.rect.centery
            if hasattr(b, 'quay_ve'):
                b.quay_ve(px)
            for ox in (-40, -20, 0, 20, 40):
                self._ds_cau.add(QuaCau(bx + ox, by, px, py))

    def _b10_bat_dau_sk3(self):

        self._b10_sk3_count += 1
        nguong_sk4 = 1 if self._b10_phase == 2 else 999

        if self._b10_sk3_count >= nguong_sk4:
            self._b10_sk3_count = 0
            self._b10_bat_dau_sk4()
            return

        b = next(iter(self.ds_boss), None)
        if not b:
            return
        px, py  = self.nhan_vat.rect.centerx, self.nhan_vat.rect.centery
        offset  = TILE_SIZE * 2 + b.rect.width // 2
        b.rect.centerx = px + offset
        b.rect.bottom  = self.nhan_vat.rect.bottom

        if hasattr(b, 'quay_ve'):
            b.quay_ve(px)

        lans = 2 if self._b10_phase == 2 else 1
        self._b10_sk3_queue = lans
        self._b10_sk3_timer = 1
        self._b10_chem_kiem()
        self._b10_sk3_queue -= 1

    def _b10_chem_kiem(self):

        b = next(iter(self.ds_boss), None)
        if not b:
            return
        bx, by = b.rect.centerx, b.rect.centery
        px, py = self.nhan_vat.rect.centerx, self.nhan_vat.rect.centery
        if hasattr(b, 'quay_ve'):
            b.quay_ve(px)
        dx = px - bx
        dy = py - by
        self._ds_kiem_bay.add(KiemBay(bx, by, dx, dy, phase=1))
                                                           
        if b.mau <= 5:
            b.mau = min(b.mau + 1, b.SO_MAU_MAX)
            self.hieu_ung.kich_hoat('troi_chan')

    def _b10_bat_dau_sk4(self):
                                           
        so_kem = 10
        self._b10_sk4_active    = True
        self._b10_sk4_dem       = 0
        self._b10_sk4_sokem     = so_kem
        self._b10_sk4_spawned   = 0
        self._b10_sk4_da_tha    = False
        self._b10_sk4_kiem_treo = []                                   

    def _b10_update_sk4(self):

        if not self._b10_sk4_active:
            return

        if self._b10_sk4_spawned < self._b10_sk4_sokem:
            self._b10_sk4_dem += 1
            interval = max(1, (1 * FPS) // self._b10_sk4_sokem)
            if self._b10_sk4_dem % interval == 0:
                map_w = len(self.ban_do[0]) * T
                idx   = self._b10_sk4_spawned
                total = self._b10_sk4_sokem
                sx    = int(map_w * (1.0 - idx / total)) - T // 2
                sx    = max(T, min(sx, map_w - T))
                k = KiemMua(sx, -T, phase=self._b10_phase)
                k.dat_huong(self.nhan_vat.rect.centerx,
                            self.nhan_vat.rect.centery)
                self._ds_kiem_mua.add(k)
                self._b10_sk4_kiem_treo.append(k)
                self._b10_sk4_spawned += 1
        elif not self._b10_sk4_da_tha:
                                                
            for k in self._b10_sk4_kiem_treo:
                k.tha()
            self._b10_sk4_kiem_treo = []
            self._b10_sk4_da_tha    = True
            self._b10_sk4_active    = False

    def _b10_phan_cong(self):
        b = next(iter(self.ds_boss), None)
        if not b:
            return
        bx, by = b.rect.centerx, b.rect.centery
        px, py = self.nhan_vat.rect.centerx, self.nhan_vat.rect.centery
        if hasattr(b, 'quay_ve'):
            b.quay_ve(px)
        dx = px - bx
        dy = py - by
        self._ds_kiem_bay.add(KiemBay(bx, by, dx, dy, phase=2))
        if abs(dx) >= abs(dy):
            self._ds_kiem_bay.add(KiemBay(bx, by, 0, 1, phase=2))
        else:
            self._ds_kiem_bay.add(KiemBay(bx, by, 1, 0, phase=2))
        self._b10_sk3_queue = 3
        self._b10_sk3_timer = 12

    def _b10_dich_sau_lung_tan_cong(self, b):

        px = self.nhan_vat.rect.centerx
        py = self.nhan_vat.rect.bottom
        KHOANG = 5
        map_w  = len(self.ban_do[0]) * T
        half_w = b.rect.width // 2

        if hasattr(self.nhan_vat, 'huong'):
            huong = self.nhan_vat.huong
        else:
            huong = 1

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
        dest_x = x_sau if du_sau else _thu_vi_tri(huong)[0]

        b.rect.centerx = dest_x
        b.rect.bottom  = self.nhan_vat.rect.bottom

        if hasattr(b, 'quay_ve'):
            b.quay_ve(px)

        self._b10_phan_cong()

    def _update_boss10(self):

        if self._b10_sk2_phase:
            self._bsk_sk2_timer -= 1
            nen_vat = list(self.ds_nen) + list(self.ds_vat)
            self._ds_kiem_bay.update(nen_vat)
            self._ds_kiem_mua.update(nen_vat)
            if self._bsk_sk2_timer <= 0:
                self._boss_hien_khoi()
                self._b10_sk2_phase = False
                if self._b10_phase == 1:
                    self._b10_phase = 2
                    self._b10_hp    = 20
                    for b in self.ds_boss:
                        b.mau        = 20
                        b.SO_MAU_MAX = 20
                        b._phase     = 2                                  
                    self._b10_sk1_next  = self._boss_timer + 5 * FPS
                    self._b10_sk1_count = 0
                    self._b10_sk3_count = 0
                    self._b10_bd_active = True
                    self._b10_bd_cd     = 0
                                                    
                    am = getattr(self, 'am_thanh', None)
                    if am and getattr(am, '_toc_do_hien', 1.0) == 1.0:
                        am.dat_toc_do(1.5)
                else:
                    self._boss_hien_khoi()
                    self._boss_win = True
                    self.da_thang  = True
                    self.ket_qua.hien_thang(self.so_man, self._so_sao_thang())
            return                                             

        self._boss_timer += 1
        bt = self._boss_timer

        nen_vat = list(self.ds_nen) + list(self.ds_vat)

        if bt >= 120 * FPS and not self.ket_qua.hien:
            self._boss_hien_khoi()
            while self.hud.tim > 0:
                self._mat_mang()
            self.ket_qua.hien_thua(self.so_man)
            return

        self._ds_kiem_bay.update(nen_vat)
        self._ds_kiem_mua.update(nen_vat)
        self._b10_update_sk4()

        if (self.tinh_linh.hien
                and self._giap_cd <= 0
                and not self.hieu_ung.dang_bat_tu):
            canh_bao = False
            vung = self.nhan_vat.rect.inflate(T * 4, T * 4)
            for c in self._ds_cau:
                if vung.colliderect(c.rect):
                    canh_bao = True; break
            if not canh_bao:
                for k in self._ds_kiem_bay:
                    if vung.colliderect(k.rect):
                        canh_bao = True; break
            if not canh_bao:
                for k in self._ds_kiem_mua:
                    if vung.colliderect(k.rect):
                        canh_bao = True; break
            if canh_bao:
                self.hieu_ung.kich_hoat('bat_tu')
                self._giap_cd = self.GIAP_CD

        if self.nhan_vat.dang_dash:
            self._i_frames = max(self._i_frames, 1)
            for b in list(self.ds_boss):
                if (self.nhan_vat.rect.colliderect(b.rect)
                        and not self._b10_dash_hit):
                    if hasattr(b, 'nhan_don'):
                        b.nhan_don()
                    self._b10_dash_hit = True
                    break
        else:
            self._b10_dash_hit = False

        if self._b10_phase == 2:
            b = next(iter(self.ds_boss), None)
            if b and b.mau <= 5 and not self._b10_enrage:
                self._b10_enrage      = True                                     
                self._b10_bd_active   = False
                self._b10_sk3_queue   = 0
                self._b10_sk4_active  = False
                self._b10_tuyet_vong_cd = 0                                  
                bx = b.rect.centerx
                px = self.nhan_vat.rect.centerx
                self.nhan_vat.vel_x = -10 if px > bx else 10
                              
                am = getattr(self, 'am_thanh', None)
                if am and getattr(am, '_toc_do_hien', 1.0) < 2.0:
                    am.dat_toc_do(2.0)

        if self._b10_enrage:
                                                      
            if not self._b10_sk4_active:
                self._b10_bat_dau_sk4()

            if self._b10_sk3_queue > 0:
                self._b10_sk3_timer -= 1
                if self._b10_sk3_timer <= 0:
                    self._b10_sk3_queue -= 1
                    self._b10_chem_kiem()
                    self._b10_sk3_timer = 20
            elif self._b10_tuyet_vong_cd > 0:
                self._b10_tuyet_vong_cd -= 1
            else:
                self._b10_sk3_queue   = 2
                self._b10_sk3_timer   = 1
                self._b10_chem_kiem()
                self._b10_sk3_queue  -= 1
                self._b10_tuyet_vong_cd = 3 * FPS

        elif self._b10_phase == 2:
            if self._b10_bd_cd > 0:
                self._b10_bd_cd -= 1
                if self._b10_bd_cd == 0:
                    self._b10_bd_active = True
            elif self._b10_bd_ne <= 0:
                self._b10_bd_active = True

            if self._b10_bd_ne > 0:
                self._b10_bd_ne -= 1
                for b in self.ds_boss:
                    map_w = len(self.ban_do[0]) * T
                    x_moi = b.rect.x + self._b10_bd_ne_dir * 6
                    x_moi_clamp = max(T, min(x_moi, map_w - T - b.rect.width))
                                                      
                    test_rect = pygame.Rect(x_moi_clamp, b.rect.top,
                                            b.rect.width, b.rect.height)
                    co_chuong = any(test_rect.colliderect(n.rect) for n in self.ds_nen)
                    bi_chan_bien = (x_moi_clamp == b.rect.x)                                   

                    if co_chuong or bi_chan_bien:
                                                                                                   
                        self._b10_bd_ne = 0
                        self._b10_dich_sau_lung_tan_cong(b)
                    else:
                        b.rect.x = x_moi_clamp

            bi_kich_hoat = self.nhan_vat.dang_dash or self._b10_f_hit
            if (self._b10_bd_active
                    and self._b10_bd_ne <= 0
                    and self._b10_sk3_queue == 0
                    and bi_kich_hoat):
                b = next(iter(self.ds_boss), None)
                if b and b.rect.inflate(3*T*2, 3*T*2).colliderect(
                        self.nhan_vat.rect):
                    px = self.nhan_vat.rect.centerx
                    self._b10_bd_ne_dir = 1 if b.rect.centerx > px else -1
                    self._b10_bd_ne     = 16
                    self._b10_bd_active = False
                    self._b10_bd_cd     = 0                                          
                    self._b10_phan_cong()

        if self._b10_enrage:
            pass                                             
        elif self._b10_sk3_queue > 0:
            self._b10_sk3_timer -= 1
            if self._b10_sk3_timer <= 0:
                self._b10_sk3_queue -= 1
                self._b10_chem_kiem()
                self._b10_sk3_timer = 20
                if self._b10_sk3_queue == 0 and self._b10_phase == 2:
                    self._b10_bd_active = True
                    self._b10_bd_cd     = 0

        elif not self.ket_qua.hien and bt >= self._b10_sk1_next:
            self._b10_sk1_count += 1
            self._b10_ban_cau()
            sk1_cd = 5 * FPS if self._b10_phase == 2 else 10 * FPS
            self._b10_sk1_next = bt + sk1_cd
            if self._b10_phase == 2:
                self._b10_bd_active = False
                self._b10_bd_cd     = 0
            if self._b10_sk1_count >= 2:
                self._b10_sk1_count = 0
                self._b10_bat_dau_sk3()

        for b in list(self.ds_boss):
            if b.da_chet() and not self._b10_sk2_phase:
                if self._b10_phase == 1:
                    b.mau        = 10
                    b.SO_MAU_MAX = 10
                    b._flash     = 0
                    b.image      = b._surf.copy()
                    b.image.set_alpha(255)
                    self._b10_sk2_phase = True
                    self._boss_an_khoi(toan_bo_san=True, thoi_gian=3 * FPS)
                else:
                    if not self.ket_qua.hien:
                        self._boss_hien_khoi()
                        self._ds_cau.empty()
                        self._ds_kiem_bay.empty()
                        self._ds_kiem_mua.empty()
                        self._boss_win = True
                        self.da_thang  = True
                        self.ket_qua.hien_thang(self.so_man, self._so_sao_thang())

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

            for k in list(self._ds_kiem_bay):
                if k.cham_nguoi(self.nhan_vat.rect) and not self.hieu_ung.dang_bat_tu:
                    k.kill()
                    go = self._mat_mang()
                    if go:
                        self._boss_hien_khoi()
                        self.ket_qua.hien_thua(self.so_man)
                    else:
                        self._i_frames = 5 * FPS
                    break

            for k in list(self._ds_kiem_mua):
                if k.cham_nguoi(self.nhan_vat.rect) and not self.hieu_ung.dang_bat_tu:
                    k.kill()
                    go = self._mat_mang()
                    if go:
                        self._boss_hien_khoi()
                        self.ket_qua.hien_thua(self.so_man)
                    else:
                        self._i_frames = 5 * FPS
                    break

        for b in list(self.ds_boss):
            if (b.cham_nguoi(self.nhan_vat.rect)
                    and not self.hieu_ung.dang_bat_tu
                    and self._i_frames <= 0):
                go = self._mat_mang()
                if go:
                    self._boss_hien_khoi()
                    self.ket_qua.hien_thua(self.so_man)
                else:
                    self._i_frames = 5 * FPS
                break