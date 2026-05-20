import pygame, math
from cai_dat import *
from the_gioi.tinh_linh import _di_chuyen_khong_xuyen

S = TILE_SIZE

class TinhLinhDieuKhien:
    """Wrapper cho tinh linh khi player hoán đổi vào điều khiển."""
    TOC_DO = 5

    def __init__(self, x, y):
        self.x     = float(x)
        self.y     = float(y)
        self._dem  = 0
        self.image = self._ve()
        self.rect  = pygame.Rect(int(x), int(y), S, S)

    def _ve(self):
        surf = pygame.Surface((S,S), pygame.SRCALPHA)
        pygame.draw.rect(surf,(80,180,255,180),(2,2,S-4,S-4),border_radius=10)
        pygame.draw.rect(surf,(160,220,255,220),(4,4,S-8,S-8),border_radius=8)
        pygame.draw.rect(surf,(230,245,255,240),(8,8,S-16,S-16),border_radius=6)
        pygame.draw.rect(surf,(255,255,255,255),(12,12,S-24,S-24),border_radius=4)
        pygame.draw.rect(surf,(255,220,0,255),(2,2,S-4,S-4),3,border_radius=10)
        return surf

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
