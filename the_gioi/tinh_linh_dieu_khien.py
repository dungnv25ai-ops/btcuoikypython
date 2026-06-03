# ============================================================
#  the_gioi/tinh_linh_dieu_khien.py — Điều khiển Tinh Linh
# ============================================================

import pygame
from cai_dat import *
from the_gioi.tinh_linh import load_bo_anh_tinh_linh, _di_chuyen_khong_xuyen, S

class TinhLinhDieuKhien:
    """Class điều khiển Tinh Linh với hệ thống 60 khung hình động"""
    TOC_DO = 5

    def __init__(self, x, y):
        # 1. Vị trí và dữ liệu ảnh
        self.x = float(x)
        self.y = float(y)
        self.data_anh = load_bo_anh_tinh_linh() 
        
        # 2. Quản lý trạng thái chuyển động
        self.trang_thai = "DUNG_TRAI"  
        self._dem_action = 0      
        
        # 3. Hình ảnh và Rect va chạm
        self.image = self.data_anh[0]
        self.rect = pygame.Rect(int(x), int(y), S, S)

    def update(self, ds_nen=None):
        """Cập nhật logic mỗi khung hình game"""
        p = pygame.key.get_pressed()
        mx = my = 0

        # --- BƯỚC 1: THU THẬP TẤT CẢ INPUT PHÍM BẤM ---
        if p[pygame.K_LEFT] or p[pygame.K_a]:
            mx -= self.TOC_DO
        if p[pygame.K_RIGHT] or p[pygame.K_d]:
            mx += self.TOC_DO
        if p[pygame.K_UP] or p[pygame.K_w]: 
            my -= self.TOC_DO
        if p[pygame.K_DOWN] or p[pygame.K_s]: 
            my += self.TOC_DO

        trang_thai_moi = self.trang_thai

        # --- BƯỚC 2: XỬ LÝ CHUYỂN ĐỔI TRẠNG THÁI CHUẨN XÁC ---
        if mx < 0:
            trang_thai_moi = "BAY_TRAI"   # Bấm trái -> Ảnh 1-15
        elif mx > 0:
            trang_thai_moi = "BAY_PHAI"   # Bấm phải -> Ảnh 31-45
        elif my != 0:
            trang_thai_moi = "BAY_TRAI"   # Chỉ bấm lên/xuống -> Dùng ảnh 1-15 theo yêu cầu
        else:
            # Khi người chơi dừng điều khiển hoàn toàn (mx == 0 và my == 0)
            if self.trang_thai == "BAY_TRAI":
                trang_thai_moi = "DUNG_TRAI"  # Dừng sau khi qua trái -> Ảnh 16-30
            elif self.trang_thai == "BAY_PHAI":
                trang_thai_moi = "DUNG_PHAI"  # Dừng sau khi qua phải -> Ảnh 46-60
            elif self.trang_thai not in ["DUNG_TRAI", "DUNG_PHAI"]:
                trang_thai_moi = "DUNG_TRAI"

        # Nếu có sự thay đổi trạng thái di chuyển, đặt lại bộ đếm khung hình
        if trang_thai_moi != self.trang_thai:
            self.trang_thai = trang_thai_moi
            self._dem_action = 0

        # --- BƯỚC 3: TÍNH TOÁN INDEX VÀ CẬP NHẬT ẢNH (Vòng lặp tuần hoàn 15 ảnh) ---
        v = self._dem_action % 15

        if self.trang_thai == "BAY_TRAI":
            idx = 0 + v    # Ảnh 1 -> 15 (Index từ 0 đến 14)
        elif self.trang_thai == "DUNG_TRAI":
            idx = 15 + v   # Ảnh 16 -> 30 (Index từ 15 đến 29)
        elif self.trang_thai == "BAY_PHAI":
            idx = 30 + v   # Ảnh 31 -> 45 (Index từ 30 đến 44)
        elif self.trang_thai == "DUNG_PHAI":
            idx = 45 + v   # Ảnh 46 -> 60 (Index từ 45 đến 59)
        else:
            idx = 15

        self._dem_action += 1
        
        # Cập nhật hình ảnh từ tài nguyên gốc (Không vẽ đè viền vàng)
        self.image = self.data_anh[idx]

        # --- BƯỚC 4: DI CHUYỂN THỰC TẾ & XỬ LÝ VA CHẠM ---
        self.x, self.y = _di_chuyen_khong_xuyen(self.x, self.y, mx, my, S, ds_nen)
        self.rect.topleft = (int(self.x), int(self.y))

    def ve(self, screen, cam_x, cam_y):
        """Vẽ Tinh Linh lên màn hình theo vị trí Camera"""
        screen.blit(self.image, (int(self.x - cam_x), int(self.y - cam_y)))