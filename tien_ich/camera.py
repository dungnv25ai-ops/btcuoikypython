# tien_ich/camera.py
from cai_dat import *


class Camera:
    def __init__(self, rong_the_gioi, cao_the_gioi):
        self.lech_x        = 0
        self.lech_y        = 0
        self.rong_the_gioi = rong_the_gioi
        self.cao_the_gioi  = cao_the_gioi
        self.ty_le         = 1.0   # zoom: <1 = thu nhỏ, 1 = bình thường

    # ── Chế độ thường: theo nhân vật ─────────────────────
    def cap_nhat(self, doi_tuong):
        self.ty_le = 1.0
        self.lech_x = doi_tuong.rect.centerx - SCREEN_W // 2
        self.lech_y = doi_tuong.rect.centery - SCREEN_H // 2
        self.lech_x = max(0, min(self.lech_x, self.rong_the_gioi - SCREEN_W))
        self.lech_y = max(0, min(self.lech_y, self.cao_the_gioi  - SCREEN_H))

    # ── Chế độ boss: zoom out vừa khít màn hình ──────────
    def cap_nhat_boss(self, man_hinh_w, man_hinh_h):
        """Tính ty_le để toàn bộ map vừa khít màn hình (letterbox)."""
        ty_le_x = man_hinh_w / self.rong_the_gioi
        ty_le_y = man_hinh_h / self.cao_the_gioi
        self.ty_le  = min(ty_le_x, ty_le_y)   # giữ tỉ lệ khung hình
        self.lech_x = 0
        self.lech_y = 0

    # ── Chế độ tinh linh ─────────────────────────────────
    def cap_nhat_vi_tri(self, cx, cy):
        self.ty_le  = 1.0
        self.lech_x = cx - SCREEN_W // 2
        self.lech_y = cy - SCREEN_H // 2
        self.lech_x = max(0, min(self.lech_x, self.rong_the_gioi - SCREEN_W))
        self.lech_y = max(0, min(self.lech_y, self.cao_the_gioi  - SCREEN_H))

    # ── Áp dụng offset (chế độ bình thường, ty_le=1) ─────
    def ap_dung(self, sprite):
        return sprite.rect.move(-self.lech_x, -self.lech_y)

    # ── Chuyển tọa độ world → screen (hỗ trợ zoom) ───────
    def world_to_screen(self, wx, wy, man_hinh_w, man_hinh_h):
        """Trả về (sx, sy) trên màn hình thực sau khi zoom."""
        sx = int(wx * self.ty_le)
        sy = int(wy * self.ty_le)
        # Căn giữa nếu map nhỏ hơn màn hình
        offset_x = (man_hinh_w - int(self.rong_the_gioi * self.ty_le)) // 2
        offset_y = (man_hinh_h - int(self.cao_the_gioi  * self.ty_le)) // 2
        return sx + max(0, offset_x), sy + max(0, offset_y)