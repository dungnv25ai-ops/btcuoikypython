                                                                               
import pygame
import math
from cai_dat import *

_CACHE_GAI = None

def _ve_gai():
    global _CACHE_GAI
    if _CACHE_GAI is not None:
        return _CACHE_GAI.copy()
    T = TILE_SIZE
    try:
        img = pygame.image.load("tai_nguyen/khoi/gai.png").convert_alpha()
        s   = pygame.transform.scale(img, (T, T))
    except Exception:
        s = pygame.Surface((T, T), pygame.SRCALPHA)
        pygame.draw.rect(s, (40, 40, 40), (0, T//2, T, T//2))
        for i in range(4):
            x = int(T/8 + i*T/4)
            pygame.draw.polygon(s, (160, 160, 160),
                                [(x-T//10, T), (x+T//10, T), (x, T//4)])
            pygame.draw.polygon(s, (220, 220, 220),
                                [(x-T//14, T-4), (x+T//14, T-4), (x, T//4+4)])
    _CACHE_GAI = s
    return s.copy()

class Gai(pygame.sprite.Sprite):
    def __init__(self, cot, hang):
        super().__init__()
        self.image = _ve_gai()
        self.rect  = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))

    def kiem_tra_cham_nguoi(self, player_rect):
        return self.rect.colliderect(player_rect)

_CACHE_NUOC = []

def _ve_nuoc(dem=0):
    global _CACHE_NUOC
    T = TILE_SIZE
    if not _CACHE_NUOC:
        for i in range(1, 61):
            try:
                img = pygame.image.load(
                    f"tai_nguyen/khoi/nuoc/{i}.png").convert_alpha()
                w_goc, h_goc = img.get_size()
                w_cat = int(w_goc * 0.6); h_cat = int(h_goc * 0.6)
                x_cat = (w_goc - w_cat) // 2; y_cat = (h_goc - h_cat) // 2
                anh_da_cat = pygame.Surface((w_cat, h_cat), pygame.SRCALPHA)
                anh_da_cat.blit(img, (0, 0), pygame.Rect(x_cat, y_cat, w_cat, h_cat))
                DO_TRAN = 4
                img_scaled = pygame.transform.scale(
                    anh_da_cat, (T + DO_TRAN, T + DO_TRAN))
                anh_final = pygame.Surface((T, T), pygame.SRCALPHA)
                anh_final.blit(img_scaled, (-(DO_TRAN//2), -(DO_TRAN//2)))
                _CACHE_NUOC.append(anh_final)
            except Exception:
                s = pygame.Surface((T, T), pygame.SRCALPHA)
                s.fill((30, 100, 200, 160))
                _CACHE_NUOC.append(s)
    return _CACHE_NUOC[(dem // 2) % len(_CACHE_NUOC)]

class KhoiNuoc(pygame.sprite.Sprite):
    def __init__(self, cot, hang):
        super().__init__()
        self._dem  = 0
        self.image = _ve_nuoc(0)
        self.rect  = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))

    def update(self):
        self._dem += 1
        self.image = _ve_nuoc(self._dem)

class KhoiDichChuyen(pygame.sprite.Sprite):
    def __init__(self, cot, hang, dich_den_cot=42, dich_den_hang=5, rong=2, cao=2):
        super().__init__()
        self._W = TILE_SIZE*rong; self._H = TILE_SIZE*cao
        
        try:
            self._surf_orig = pygame.image.load("tai_nguyen/khoi/cong.png").convert_alpha()
            self._surf_orig = pygame.transform.scale(self._surf_orig, (self._W, self._H))
        except Exception:
                                  
            self._surf_orig = pygame.Surface((self._W, self._H), pygame.SRCALPHA)
            pygame.draw.rect(self._surf_orig, (100,30,180), (0,0,self._W,self._H), border_radius=8)
            pygame.draw.rect(self._surf_orig, (140,70,220), (2,2,self._W-4,self._H-4), border_radius=7)
            cx, cy = self._W//2, self._H//2
            pygame.draw.circle(self._surf_orig, (180,120,255), (cx, cy), min(self._W,self._H)//2-10)

        self.image = self._surf_orig.copy()
                                                          
        self.rect  = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        
        self.dem             = 0
        self.dich_cot        = dich_den_cot
        self.dich_hang       = dich_den_hang
        self._cot_cong       = cot
        self._hang_cong      = hang
        self._trong_vung     = False
        self._hoi_thoai_hien = False
        self._cho_tra_loi    = False
        self.font            = None

    def _init_font(self):
        if not self.font:
            self.font = pygame.font.SysFont(FONT_CHINH, 16)

    def update(self):
                                                              
        self.dem += 1

    def xu_ly_vung(self, player_rect):
        dang_trong = self.rect.inflate(TILE_SIZE, TILE_SIZE).colliderect(player_rect)
        if dang_trong and not self._trong_vung:
            self._hoi_thoai_hien = True
            self._cho_tra_loi    = True
        if not dang_trong and self._trong_vung:
            self._hoi_thoai_hien = False
            self._cho_tra_loi    = False
        self._trong_vung = dang_trong
        return self._hoi_thoai_hien

    def tra_loi_co(self, player_rect=None):
        self._hoi_thoai_hien = False
        self._cho_tra_loi    = False
        if player_rect is not None:
            if player_rect.centerx > (self._cot_cong + 2) * TILE_SIZE:
                return ((self._cot_cong - 3) * TILE_SIZE, self.dich_hang * TILE_SIZE)
        return (self.dich_cot * TILE_SIZE, self.dich_hang * TILE_SIZE)

    def tra_loi_khong(self):
        self._hoi_thoai_hien = False
        self._cho_tra_loi    = False

    def ve_hoi_thoai(self, screen, cam_x, cam_y, mw, mh):
        if not self._hoi_thoai_hien:
            return
        self._init_font()
        font_to = pygame.font.SysFont(FONT_CHINH, 18, bold=True)
        cx = self.rect.centerx - cam_x
        cy = self.rect.top     - cam_y - 10
        BW, BH = 300, 100
        bx = max(8, min(cx-BW//2, mw-BW-8))
        by = max(8, cy-BH-10)
        bong = pygame.Surface((BW, BH), pygame.SRCALPHA)
        pygame.draw.rect(bong, (20,10,40,230),   (0,0,BW,BH), border_radius=10)
        pygame.draw.rect(bong, (180,100,255,255), (0,0,BW,BH), 2, border_radius=10)
        screen.blit(bong, (bx, by))
        t1 = font_to.render("Ban co muon di vao khong?", True, (220,180,255))
        screen.blit(t1, t1.get_rect(center=(bx+BW//2, by+28)))
        for i, (lbl, mau) in enumerate([("Y  Co",(80,200,80)), ("N  Khong",(200,80,80))]):
            rr = pygame.Rect(bx+30+i*150, by+58, 110, 30)
            hv = rr.collidepoint(pygame.mouse.get_pos())
            pygame.draw.rect(screen,
                             tuple(min(c+40,255) for c in mau) if hv else mau,
                             rr, border_radius=6)
            t2 = self.font.render(lbl, True, TRANG)
            screen.blit(t2, t2.get_rect(center=rr.center))
        self._rect_co    = pygame.Rect(bx+30,  by+58, 110, 30)
        self._rect_khong = pygame.Rect(bx+180, by+58, 110, 30)

    def xu_ly_click_hoi_thoai(self, ev_pos):
        if not self._cho_tra_loi:
            return None
        if hasattr(self, '_rect_co')    and self._rect_co.collidepoint(ev_pos):
            return 'co'
        if hasattr(self, '_rect_khong') and self._rect_khong.collidepoint(ev_pos):
            return 'khong'
        return None