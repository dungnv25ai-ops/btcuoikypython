                       
import pygame, math, time, os
from cai_dat import *

S = int(TILE_SIZE * 0.8)

_BO_ANH_60=[]
def load_bo_anh_tinh_linh():
    global _BO_ANH_60
    if not _BO_ANH_60:
        thu_muc_goc = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for i in range(1, 61):
            ten_file = f"{i}.png" 
            duong_dan = os.path.join(thu_muc_goc, "tai_nguyen", "hinh_anh","tinh_linh", ten_file)
            try:
                anh = pygame.image.load(duong_dan).convert_alpha()
                _BO_ANH_60.append(pygame.transform.scale(anh, (S, S)))
            except:
                tam = pygame.Surface((S, S), pygame.SRCALPHA)
                pygame.draw.rect(tam, (100, 200, 255, 100), (0, 0, S, S), border_radius=8)
                _BO_ANH_60.append(tam)
    return _BO_ANH_60

def _get():
    return load_bo_anh_tinh_linh()[0]

def _di_chuyen_khong_xuyen(x, y, mx, my, size, ds_nen):

    if not ds_nen:
        return x + mx, y + my

    nx = x + mx
    r  = pygame.Rect(int(nx), int(y), size, size)
    for n in ds_nen:
        if r.colliderect(n.rect):
            if mx > 0: nx = float(n.rect.left - size)
            elif mx < 0: nx = float(n.rect.right)
            mx = 0; break

    ny = y + my
    r  = pygame.Rect(int(nx), int(ny), size, size)
    for n in ds_nen:
        if r.colliderect(n.rect):
            if my > 0: ny = float(n.rect.top - size)
            elif my < 0: ny = float(n.rect.bottom)
            my = 0; break

    return nx, ny

class TinhLinh:
    def __init__(self):
        self.x = self.y = 0.0
        self.hien         = False
        self.quy_dao      = 0.0
        self.dem          = 0

        self.data_anh     = load_bo_anh_tinh_linh()
        self.image        = self.data_anh[0]
        self.trang_thai   = "DUNG_TRAI"
        self._dem_action  = 0

    def bat_dau(self, x, y):
        self.x, self.y = float(x), float(y)
        self.hien = True

    def update(self, player_rect, ds_nen=None):
        if not self.hien: return
        self.dem += 1; self.quy_dao += 0.025

        mx = my = 0

        cx = player_rect.centerx + math.cos(self.quy_dao)*55
        cy = player_rect.top - 12 + math.sin(self.quy_dao*1.3)*16
        mx = (cx-self.x)*0.06
        my = (cy-self.y)*0.06
        self.x, self.y = _di_chuyen_khong_xuyen(
            self.x, self.y, mx, my, S, ds_nen)

        trang_thai_moi = self.trang_thai

        if mx < -0.1:
            trang_thai_moi = "BAY_TRAI"
        elif mx > 0.1:
            trang_thai_moi = "BAY_PHAI"
        elif abs(my) > 0.1:
                                                                          
            trang_thai_moi = "BAY_TRAI"
        else:
                                                                          
            if self.trang_thai == "BAY_TRAI":
                trang_thai_moi = "DUNG_TRAI"
            elif self.trang_thai == "BAY_PHAI":
                trang_thai_moi = "DUNG_PHAI"
            elif self.trang_thai not in ["DUNG_TRAI", "DUNG_PHAI"]:
                trang_thai_moi = "DUNG_TRAI"

        if trang_thai_moi != self.trang_thai:
            self.trang_thai = trang_thai_moi
            self._dem_action = 0

        v = self._dem_action % 15
        if self.trang_thai == "BAY_TRAI":
            idx = 0 + v                           
        elif self.trang_thai == "DUNG_TRAI":
            idx = 15 + v                            
        elif self.trang_thai == "BAY_PHAI":
            idx = 30 + v                            
        elif self.trang_thai == "DUNG_PHAI":
            idx = 45 + v                            
        else:
            idx = 15

        self.image = self.data_anh[idx]
        self._dem_action += 1

    def ve(self, screen, cam_x, cam_y, mw=0, mh=0):
        if not self.hien: return
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)
              
        alpha = int(40+25*math.sin(self.dem*0.07))
        rg    = int(28+6*math.sin(self.dem*0.05))
        g = pygame.Surface((rg*2,rg*2),pygame.SRCALPHA)
        pygame.draw.circle(g,(80,200,255,alpha),(rg,rg),rg)
        screen.blit(g,(sx-rg+S//2,sy-rg+S//2))
        
        screen.blit(self.image, (sx, sy))