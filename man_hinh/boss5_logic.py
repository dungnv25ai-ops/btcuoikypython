# man_hinh/boss5_logic.py
# Mixin chứa toàn bộ skill và logic chiến đấu Boss 5.
#
# Lịch skill (tính từ giây 0):
#   Giây  3 : Trói chân player (3s)
#   Giây  5 : SK1 — bắn 5 cầu, lặp lại mỗi 10s
#   Giây  8 : Đóng băng player
#   Giây 10 : SK3 — dịch chuyển + bắn tia laser 1 giây
#   Giây 25 : Mở bay + tinh linh thoại
#   Giây 30 : SK2 — ẩn sàn 5s
#   Giây 60 : Thắng

import pygame
import math
from cai_dat import *
from the_gioi.vat_the import QuaCau, KeDiChuyen, TiaBan

T = TILE_SIZE


class Boss5LogicMixin:
    """Tất cả skill + update loop boss màn 5."""

    # ── SK1: bắn 5 cầu ───────────────────────────────────
    def _boss_sk1_ban(self):
        for b in self.ds_boss:
            bx, by = b.rect.centerx, b.rect.centery
            px, py = self.nhan_vat.rect.centerx, self.nhan_vat.rect.centery
            if hasattr(b, 'quay_ve'):
                b.quay_ve(px)
            for ox in (-40, -20, 0, 20, 40):
                self._ds_cau.add(QuaCau(bx + ox, by, px, py))

    # ── SK3: dịch chuyển + bắn tia laser ─────────────────
    def _boss_sk3_thuc_hien(self):
        """Dịch chuyển boss ra sau lưng hoặc trước mặt player 5px,
        rồi bắn tia laser 1x10 tile về phía player."""
        b = next(iter(self.ds_boss), None)
        if not b:
            return

        px  = self.nhan_vat.rect.centerx
        py  = self.nhan_vat.rect.centery
        KHOANG = 10   # px cách player

        map_w = len(self.ban_do[0]) * T
        map_h = len(self.ban_do)    * T

        # Thử đặt sau lưng (ngược hướng nhìn của player)
        # Hướng player: huong = 1 (nhìn phải) → sau lưng = bên trái
        if hasattr(self.nhan_vat, 'huong'):
            huong = self.nhan_vat.huong
        else:
            huong = 1

        # Sau lưng = phía ngược hướng nhìn
        x_sau = px - huong * (b.rect.width // 2 + KHOANG)
        x_sau = max(T, min(x_sau, map_w - b.rect.width - T))

        # Kiểm tra có tile chặn không ở vị trí sau lưng
        test_rect = pygame.Rect(x_sau - b.rect.width // 2,
                                b.rect.top,
                                b.rect.width, b.rect.height)
        co_chuong = any(test_rect.colliderect(n.rect) for n in self.ds_nen)

        if not co_chuong:
            dest_x = x_sau
        else:
            # Trước mặt player
            x_truoc = px + huong * (b.rect.width // 2 + KHOANG)
            x_truoc = max(T, min(x_truoc, map_w - b.rect.width - T))
            dest_x  = x_truoc

        # Dịch chuyển boss
        b.rect.centerx = dest_x
        b.rect.bottom  = self.nhan_vat.rect.bottom

        # Quay mặt boss về phía player sau khi dịch chuyển
        if hasattr(b, 'quay_ve'):
            b.quay_ve(px)

        # Bắn tia laser từ tâm boss về tâm player
        bx = b.rect.centerx
        by = b.rect.centery
        tia = TiaBan(bx, by, px, py)
        self._ds_tia_ban.add(tia)

    # ── SK2: ẩn/hiện sàn ─────────────────────────────────
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

    # ── Update loop boss 5 ────────────────────────────────
    def _update_boss5(self):
        if not self.ds_boss:
            return

        # ── SK2 đang active: dừng đồng hồ, không tăng timer ─
        if self._bsk_sk2_active:
            self._bsk_sk2_timer -= 1
            if self._bsk_sk2_timer <= 0:
                self._boss_hien_khoi()
            # Vẫn update + check va chạm tia bắn đang bay
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
            return   # không tăng bt

        self._boss_timer += 1
        bt = self._boss_timer

        # ── Khởi tạo ds_tia_ban nếu chưa có ─────────────
        if not hasattr(self, '_ds_tia_ban'):
            self._ds_tia_ban = pygame.sprite.Group()

        # ── Trói chân: giây 3,13,23,33,43,53 ────────────
        if bt in (3*FPS, 13*FPS, 23*FPS, 33*FPS, 43*FPS, 53*FPS):
            if hasattr(self, 'hieu_ung'):
                self.hieu_ung.kich_hoat('troi_chan')

        # ── Còn 30s: tăng nhạc x1.5 ─────────────────────
        if bt == 30 * FPS:
            am = getattr(self, 'am_thanh', None)
            if am and getattr(am, '_toc_do_hien', 1.0) == 1.0:
                am.dat_toc_do(1.5)

        # ── SK1: giây 5, mỗi 10s ─────────────────────────
        if bt == self._bsk_sk1_next:
            self._boss_sk1_ban()
            self._bsk_sk1_next += 10 * FPS

        # ── Đóng băng: giây 7, 17, 37, 47, 52 ───────────
        if bt in (7*FPS, 17*FPS, 37*FPS, 47*FPS, 52*FPS):
            if hasattr(self, 'hieu_ung'):
                self.hieu_ung.kich_hoat('dong_bang')

        # ── SK3: giây 10, 20, 40, 50, 55 ────────────────
        if bt in (10*FPS, 20*FPS, 40*FPS, 50*FPS, 55*FPS):
            self._boss_sk3_thuc_hien()

        # ── Giây 25: Mở bay ───────────────────────────────
        if bt == 25 * FPS and not self._bsk_sk2_done:
            if not self.nhan_vat.co_bay:
                self.nhan_vat.co_bay = True
                pygame.event.post(pygame.event.Event(
                    pygame.USEREVENT, {'code': 'bay_unlock'}))

        # ── Giây 30: SK2 ẩn sàn ──────────────────────────
        if bt >= 30 * FPS and not self._bsk_sk2_done:
            self._bsk_sk2_done = True
            self._boss_an_khoi()

        # ── Update tia bắn ────────────────────────────────
        from the_gioi.nen_tang import KhoiTanHinh
        nen_vat = [n for n in list(self.ds_nen) + list(self.ds_vat)
                   if not isinstance(n, KhoiTanHinh)]
        self._ds_tia_ban.update(nen_vat)

        # ── Tinh linh tự dùng bất tử khi sắp bị trúng ───
        # Chỉ map 5, khi bất tử đã hồi và có projectile gần player
        if (self.so_man == 5
                and self.tinh_linh.hien
                and self._giap_cd <= 0
                and not self.hieu_ung.dang_bat_tu):
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
                self._tinh_linh_noi("Hay can than!")

        # ── Va chạm tia bắn với player ────────────────────
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

        # ── Va chạm quả cầu với player ────────────────────
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

        # ── Chạm boss trực tiếp ───────────────────────────
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

        # ── Giây 60: Thắng ───────────────────────────────
        if bt >= 60 * FPS and not self.ket_qua.hien:
            self._boss_hien_khoi()
            self._ds_tia_ban.empty()
            self._boss_win = True
            self.da_thang  = True
            self.ket_qua.hien_thang(self.so_man, self._so_sao_thang())
