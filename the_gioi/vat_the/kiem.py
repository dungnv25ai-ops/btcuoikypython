# the_gioi/vat_the/kiem.py — Kiếm vật phẩm + Sách mở Dash
import pygame
import math
from cai_dat import *


# ── Vẽ kiếm ──────────────────────────────────────────────
def _ve_kiem(ngang=False):
    W, H = (TILE_SIZE*2, TILE_SIZE) if ngang else (TILE_SIZE, TILE_SIZE*2)
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    pygame.draw.rect(s, (220, 200, 30), (0, 0, W, H), border_radius=4)
    pygame.draw.rect(s, (150, 120, 10), (0, 0, W, H), 2, border_radius=4)
    return s


class Kiem(pygame.sprite.Sprite):
    """Kiếm 1x2 — nhấn F khi gần để nhặt (biến mất)."""
    PHAM_VI = TILE_SIZE * 2

    def __init__(self, cot, hang, ngang=False):
        super().__init__()
        self.ngang       = ngang
        self.image       = _ve_kiem(ngang)
        self.rect        = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self.dem_nhip    = 0
        self._alpha      = 255
        self._bien_mat   = False
        self._alpha_giam = 0

    def gan_nguoi_choi(self, player_rect):
        return self.rect.inflate(self.PHAM_VI*2, self.PHAM_VI*2).colliderect(player_rect)

    def bat_dau_bien_mat(self):
        self._bien_mat   = True
        self._alpha_giam = 18

    def update(self):
        self.dem_nhip += 1
        if not self._bien_mat:
            a = int(220 + 35*math.sin(self.dem_nhip*0.08))
            self.image.set_alpha(a)
        else:
            self._alpha = max(0, self._alpha - self._alpha_giam)
            self.image.set_alpha(self._alpha)
            if self._alpha <= 0:
                self.kill()

    def ve_hint(self, screen, cam_x, cam_y, font):
        t  = font.render("[F] Nhat kiem", True, VANG)
        x  = self.rect.centerx - cam_x - t.get_width()//2
        y  = self.rect.top - cam_y - 22
        bg = pygame.Surface((t.get_width()+8, t.get_height()+4), pygame.SRCALPHA)
        pygame.draw.rect(bg, (0, 0, 0, 140), (0, 0, *bg.get_size()), border_radius=4)
        screen.blit(bg, (x-4, y-2))
        screen.blit(t, (x, y))


# ── Vẽ sách ──────────────────────────────────────────────
def _ve_sach():
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(s, (30, 100, 200),  (2, 2, TILE_SIZE-4, TILE_SIZE-4), border_radius=5)
    pygame.draw.rect(s, (60, 140, 240),  (4, 4, TILE_SIZE-8, TILE_SIZE-8), border_radius=4)
    pygame.draw.rect(s, (240, 235, 200), (8, 6, TILE_SIZE-16, TILE_SIZE-10), border_radius=3)
    for i in range(3):
        pygame.draw.rect(s, (150, 140, 100), (10, 12+i*8, TILE_SIZE-22, 3))
    pygame.draw.rect(s, (20, 70, 160), (2, 2, 5, TILE_SIZE-4), border_radius=3)
    pts = [(TILE_SIZE-14, 8), (TILE_SIZE-8, 20),
           (TILE_SIZE-13, 20), (TILE_SIZE-7, TILE_SIZE-8)]
    pygame.draw.polygon(s, (255, 230, 50), pts)
    pygame.draw.polygon(s, (200, 170, 20), pts, 1)
    pygame.draw.rect(s, (15, 60, 140), (0, 0, TILE_SIZE, TILE_SIZE), 2, border_radius=5)
    return s


class Sach1x1(pygame.sprite.Sprite):
    """Sách 1x1 — nhặt bằng F, mở khóa Dash."""
    PHAM_VI = TILE_SIZE * 2

    def __init__(self, cot, hang):
        super().__init__()
        self.image     = _ve_sach()
        self.rect      = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self.dem       = 0
        self._bien_mat = False
        self._alpha    = 255

    def gan_nguoi_choi(self, player_rect):
        return self.rect.inflate(self.PHAM_VI*2, self.PHAM_VI*2).colliderect(player_rect)

    def bat_dau_bien_mat(self):
        self._bien_mat = True

    def update(self):
        self.dem += 1
        if not self._bien_mat:
            a = int(210 + 45*math.sin(self.dem*0.09))
            self.image.set_alpha(a)
        else:
            self._alpha = max(0, self._alpha - 18)
            self.image.set_alpha(self._alpha)
            if self._alpha <= 0:
                self.kill()

    def ve_hint(self, screen, cam_x, cam_y, font):
        t  = font.render("[F] Nhan sach: mo khoa Dash", True, (100, 200, 255))
        x  = self.rect.centerx - cam_x - t.get_width()//2
        y  = self.rect.top - cam_y - 22
        bg = pygame.Surface((t.get_width()+8, t.get_height()+4), pygame.SRCALPHA)
        pygame.draw.rect(bg, (0, 0, 0, 140), (0, 0, *bg.get_size()), border_radius=4)
        screen.blit(bg, (x-4, y-2))
        screen.blit(t, (x, y))
