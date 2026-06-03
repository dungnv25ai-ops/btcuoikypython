# man_hinh/boss5_logic.py
# Mixin chứa toàn bộ skill và logic chiến đấu Boss 5.
# ManChoi kế thừa class này TRƯỚC ManChoiBase.
#
# Các thuộc tính ManChoi cần có sẵn khi gọi:
#   self.ds_boss, self.ds_nen, self.ds_ke, self._ds_cau
#   self.nhan_vat, self.hud, self.ket_qua
#   self._bsk_sk1_next, self._bsk_sk2_done, self._bsk_sk2_active
#   self._bsk_sk2_timer, self._bsk_khoi_an, self._bsk_ke_an
#   self._giap_active, self._i_frames, self._boss_timer
#   self.ban_do, self.so_man

import pygame
from cai_dat import *
from the_gioi.vat_the import QuaCau, KeDiChuyen

T = TILE_SIZE


class Boss5LogicMixin:
    """Tất cả skill + update loop boss màn 5."""

    # ── Skill helpers dùng chung với boss10 ───────────────
    def _boss_sk1_ban(self):
        """SK1: bắn 5 quả cầu từ boss hướng về player."""
        for b in self.ds_boss:
            bx, by = b.rect.centerx, b.rect.centery
            px, py = self.nhan_vat.rect.centerx, self.nhan_vat.rect.centery
            for ox in (-40, -20, 0, 20, 40):
                self._ds_cau.add(QuaCau(bx + ox, by, px, py))

    def _boss_an_khoi(self, toan_bo_san=False):
        """SK2: ẩn toàn bộ tile + lưu/kill quái."""
        hidden_tiles = list(self.ds_nen)
        for tile in hidden_tiles:
            self.ds_nen.remove(tile)

        hidden_ke = []
        for ke in list(self.ds_ke):
            hidden_ke.append({
                'cot':  ke.rect.x // T,
                'hang': ke.rect.y // T,
                'co_tan_cong': ke.co_tan_cong,
            })
            ke.kill()

        self._bsk_khoi_an    = hidden_tiles
        self._bsk_ke_an      = hidden_ke
        self._bsk_sk2_active = True
        self._bsk_sk2_timer  = 5 * FPS

    def _boss_hien_khoi(self):
        """Restore tile và hồi sinh quái."""
        for tile in getattr(self, '_bsk_khoi_an', []):
            self.ds_nen.add(tile)
        self._bsk_khoi_an = []

        for ke_info in getattr(self, '_bsk_ke_an', []):
            ke = KeDiChuyen(
                ke_info['cot'], ke_info['hang'],
                ke_info['cot'] - 10, ke_info['cot'] + 10,
                co_tan_cong=ke_info['co_tan_cong'])
            ke.mau = 3
            self.ds_ke.add(ke)
        self._bsk_ke_an      = []
        self._bsk_sk2_active = False
        self._bsk_sk2_timer  = 0

    # ── Update loop boss 5 ────────────────────────────────
    def _update_boss5(self):
        """Gọi từ ManChoi.update() khi so_man == 5."""
        if not self.ds_boss:
            return

        self._boss_timer += 1
        bt = self._boss_timer

        # ── SK1: từ giây 5, mỗi 10s bắn 5 cầu ───────────
        if bt == self._bsk_sk1_next:
            self._boss_sk1_ban()
            self._bsk_sk1_next += 10 * FPS

        # ── Giây 25: mở skill bay + tinh linh thoại báo trước ──
        if bt == 25 * FPS and not self._bsk_sk2_done:
            if not self.nhan_vat.co_bay:
                self.nhan_vat.co_bay = True
                pygame.event.post(pygame.event.Event(
                    pygame.USEREVENT, {'code': 'bay_unlock'}))
            # Kích tinh linh nói (nếu chưa nói)
            if hasattr(self, 'tinh_linh') and self.tinh_linh.hien                     and not self.tinh_linh.dang_noi:
                self.tinh_linh.kich_hoat_thoai()

        # ── Giây 30: ẩn khối 5s (sau khi thoại 5 giây) ──
        if bt >= 30 * FPS and not self._bsk_sk2_done:
            self._bsk_sk2_done = True
            self._boss_an_khoi()

        if self._bsk_sk2_active:
            self._bsk_sk2_timer -= 1
            if self._bsk_sk2_timer <= 0:
                self._boss_hien_khoi()

        # ── Cầu chạm player ───────────────────────────────
        if self._i_frames <= 0:
            for c in list(self._ds_cau):
                if c.cham_nguoi(self.nhan_vat.rect) and not self._giap_active:
                    c.kill()
                    go = self.hud.mat_mang()
                    if go:
                        self._boss_hien_khoi()
                        self.ket_qua.hien_thua(self.so_man)
                    else:
                        self._i_frames = 5 * FPS
                    break

        # ── Chạm boss trực tiếp → bất tử 5s ─────────────
        for b in self.ds_boss:
            if (b.cham_nguoi(self.nhan_vat.rect)
                    and self._i_frames <= 0
                    and not self._giap_active):
                go = self.hud.mat_mang()
                if go:
                    self._boss_hien_khoi()
                    self.ket_qua.hien_thua(self.so_man)
                else:
                    self._i_frames = 5 * FPS
                break

        # ── Sống sót 60s → thắng ─────────────────────────
        if bt >= 60 * FPS and not self.ket_qua.hien:
            self._boss_hien_khoi()
            self._boss_win = True
            self.da_thang  = True
            self.ket_qua.hien_thang(self.so_man, self.hud.sao)