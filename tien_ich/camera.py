# ============================================================
#  tien_ich/camera.py — Camera cuộn theo nhân vật
# ============================================================

from cai_dat import *


class Camera:
    def __init__(self, rong_the_gioi, cao_the_gioi):
        self.lech_x       = 0
        self.lech_y       = 0
        self.rong_the_gioi = rong_the_gioi
        self.cao_the_gioi  = cao_the_gioi

    def cap_nhat(self, doi_tuong):
        """Giữ nhân vật ở giữa màn hình."""
        self.lech_x = doi_tuong.rect.centerx - SCREEN_W // 2
        self.lech_y = doi_tuong.rect.centery - SCREEN_H // 2

        # Không cuộn ra ngoài biên map
        self.lech_x = max(0, min(self.lech_x, self.rong_the_gioi - SCREEN_W))
        self.lech_y = max(0, min(self.lech_y, self.cao_the_gioi  - SCREEN_H))

    def ap_dung(self, sprite):
        """Trả về rect đã trừ offset camera → dùng để vẽ."""
        return sprite.rect.move(-self.lech_x, -self.lech_y)

    def cap_nhat_vi_tri(self, cx, cy):
        """Căn camera theo tọa độ bất kỳ (dùng khi điều khiển tinh linh)."""
        self.lech_x = cx - SCREEN_W // 2
        self.lech_y = cy - SCREEN_H // 2
        self.lech_x = max(0, min(self.lech_x, self.rong_the_gioi - SCREEN_W))
        self.lech_y = max(0, min(self.lech_y, self.cao_the_gioi  - SCREEN_H))
