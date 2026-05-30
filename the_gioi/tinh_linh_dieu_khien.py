# the_gioi/tinh_linh_dieu_khien.py
import pygame, math
from cai_dat import *
# Import hàm _get để lấy ảnh png và hàm di chuyển
from the_gioi.tinh_linh import _get, _di_chuyen_khong_xuyen

S = TILE_SIZE // 2   # 0.5 tile

class TinhLinhDieuKhien:
    """Wrapper cho tinh linh khi player hoán đổi vào điều khiển."""
    TOC_DO = 5

    def __init__(self, x, y):
        self.x     = float(x)
        self.y     = float(y)
        self._dem  = 0
        
        # 1. Lấy ảnh gốc tinhlinh.png
        anh_goc = _get().copy()
        # 2. Vẽ đè viền vàng (độ dày 3px) lên trên để đánh dấu đang được điều khiển
        pygame.draw.rect(anh_goc, (255, 220, 0, 255), (0, 0, S, S), 3, border_radius=8)
        self.image = anh_goc
        
        self.rect  = pygame.Rect(int(x), int(y), S, S)

    # ... (Giữ nguyên vòng lặp update() và các hàm xử lý nút bên dưới của bạn) ...
    def update(self, ds_nen=None):
        self._dem += 1
        p  = pygame.key.get_pressed()
        mx = my = 0
        if p[pygame.K_LEFT]  or p[pygame.K_a]: mx -= self.TOC_DO
        if p[pygame.K_RIGHT] or p[pygame.K_d]: mx += self.TOC_DO
        if p[pygame.K_UP]    or p[pygame.K_w]: my -= self.TOC_DO
        if p[pygame.K_DOWN]  or p[pygame.K_s]: my += self.TOC_DO

        self.x, self.y = _di_chuyen_khong_xuyen(
            self.x, self.y, mx, my, S, ds_nen)
        self.rect.topleft = (int(self.x), int(self.y))

    def ve(self, screen, cam_x, cam_y):
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)
        # Glow nhịp đập
        r  = int(22+6*math.sin(self._dem*0.1))
        a  = int(50+30*math.sin(self._dem*0.08))
        g  = pygame.Surface((r*2,r*2),pygame.SRCALPHA)
        pygame.draw.circle(g,(100,200,255,a),(r,r),r)
        screen.blit(g,(sx-r+S//2, sy-r+S//2))
        screen.blit(self.image,(sx,sy))
