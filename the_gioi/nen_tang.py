                      
import pygame, os
from cai_dat import *

def _khoi(mc, ms, mt, ky=""):
    s=pygame.Surface((TILE_SIZE,TILE_SIZE))
    s.fill(mc)
    pygame.draw.rect(s,mt,(0,0,TILE_SIZE,TILE_SIZE),2)
    return s

_C={}
def _g(k,fn):
    if k not in _C: _C[k]=fn()
    return _C[k].copy()

_THU_MUC_KHOI = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "tai_nguyen", "khoi")

_ANH_CACHE = {}                  

def _tai_anh_khoi(ten_file, xoay=0):

    key = f"{ten_file}_{xoay}"
    if key in _ANH_CACHE:
        return _ANH_CACHE[key].copy()
    path = os.path.join(_THU_MUC_KHOI, ten_file)
    if os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            if xoay != 0:
                img = pygame.transform.rotate(img, xoay)
                                                                         
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            _ANH_CACHE[key] = img
            return img.copy()
        except Exception:
            pass
    return None                   

def _tile(ten_file, xoay=0, mau_fallback=(70,150,40)):

    img = _tai_anh_khoi(ten_file, xoay)
    if img:
        return img
    s = pygame.Surface((TILE_SIZE, TILE_SIZE))
    s.fill(mau_fallback)
    return s

class NenTang(pygame.sprite.Sprite):

    def __init__(self, c, r):
        super().__init__()
        self.image = _g("dat", lambda: _tile("dat.png", mau_fallback=(70,150,40)))
        self.rect  = self.image.get_rect(topleft=(c*TILE_SIZE, r*TILE_SIZE))

class NenTangBoss(pygame.sprite.Sprite):
    def __init__(self, c, r):
        super().__init__()
        self.image = _g("boss", lambda: _khoi((70,70,85),(100,100,120),(40,40,55)))
        self.rect  = self.image.get_rect(topleft=(c*TILE_SIZE, r*TILE_SIZE))

class KhucGo(pygame.sprite.Sprite):
    def __init__(self, c, r):
        super().__init__()
        self.image = _g("go", lambda: _tile("go.png", mau_fallback=(150, 95, 35)))
        self.rect  = self.image.get_rect(topleft=(c*TILE_SIZE, r*TILE_SIZE))

_THU_MUC_LA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'tai_nguyen',  'khoi', 'la')

_ANH_LA = []                                

def _load_anh_la():

    global _ANH_LA
    if _ANH_LA:
        return _ANH_LA
    if not os.path.isdir(_THU_MUC_LA):
        return _ANH_LA
    for i in range(1, 61):
        path = os.path.join(_THU_MUC_LA, f"{i}.png")
        if not os.path.isfile(path):
            break
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            _ANH_LA.append(img)
        except Exception:
            pass
    return _ANH_LA

class TileCo(pygame.sprite.Sprite):

    def __init__(self, c, r):
        super().__init__()
        self.image = _g("co", lambda: _tile("co.png", mau_fallback=(60,180,60)))
        self.rect  = self.image.get_rect(topleft=(c*TILE_SIZE, r*TILE_SIZE))

class TileCoTrai(pygame.sprite.Sprite):

    def __init__(self, c, r):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect  = self.image.get_rect(topleft=(c*TILE_SIZE, r*TILE_SIZE))

class TileCoPhai(pygame.sprite.Sprite):

    def __init__(self, c, r):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect  = self.image.get_rect(topleft=(c*TILE_SIZE, r*TILE_SIZE))

class KhoiTanHinh(pygame.sprite.Sprite):

    def __init__(self, c, r):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect  = self.image.get_rect(topleft=(c*TILE_SIZE, r*TILE_SIZE))

import math as _math

class SaoMap(pygame.sprite.Sprite):

    def __init__(self, c, r):
        super().__init__()
        S = TILE_SIZE
        self._dem = 0
        self.image = pygame.Surface((S, S), pygame.SRCALPHA)
        self.rect  = self.image.get_rect(topleft=(c*S, r*S))
        self._ve()

    def _ve(self):
        S = TILE_SIZE; cx = cy = S // 2
        pts = []
        for i in range(10):
            a  = _math.radians(-90 + i*36)
            ri = cx - 4 if i % 2 == 0 else cx // 2
            pts.append((cx + ri*_math.cos(a), cy + ri*_math.sin(a)))
        self.image.fill((0, 0, 0, 0))
        pygame.draw.polygon(self.image, (255, 215, 0), pts)
        pygame.draw.polygon(self.image, (255, 255, 120), pts, 2)

    def update(self):
        self._dem += 1
        self.image.set_alpha(int(180 + 75*abs(_math.sin(self._dem*0.06))))

class TileLa(pygame.sprite.Sprite):

    _SPD = 2

    def __init__(self, c, r):
        super().__init__()
                                       
        self.rect    = pygame.Rect(c*TILE_SIZE, (r-1)*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self._anh_la = _load_anh_la()
        self._dem    = 0
                                                                     
        self._pha    = (c * 7) % max(1, len(self._anh_la)) if self._anh_la else 0
        self.image   = self._lay_anh()

    def _lay_anh(self):

        anh = self._anh_la
        if not anh:
            s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(s, (60, 200, 60, 180),
                             (0, TILE_SIZE//2, TILE_SIZE, TILE_SIZE//2),
                             border_radius=4)
            return s
        n   = len(anh)                                               
        ck  = (n - 1) * 2                                           
                                                              
        v   = ((self._dem // self._SPD) + self._pha) % ck
        idx = v if v < n else ck - v
        return anh[idx]

    def update(self):
        self._dem += 1
        self.image = self._lay_anh()

class Sach(pygame.sprite.Sprite):

    def __init__(self,c,r):
        super().__init__()
        s=pygame.Surface((TILE_SIZE,TILE_SIZE*3),pygame.SRCALPHA)
                           
        pygame.draw.rect(s,(100,80,40),(TILE_SIZE//2-4,0,8,TILE_SIZE*3))
        pygame.draw.rect(s,(130,105,55),(TILE_SIZE//2-3,0,3,TILE_SIZE*3))
                               
        for y in [TILE_SIZE//2, TILE_SIZE+TILE_SIZE//2, TILE_SIZE*2+TILE_SIZE//2]:
            pygame.draw.rect(s,(160,120,60),(TILE_SIZE//2-14,y-4,28,8),border_radius=3)
            pygame.draw.rect(s,(190,150,80),(TILE_SIZE//2-13,y-3,26,3))
                              
        bx,by=TILE_SIZE//2-10,TILE_SIZE-10
        pygame.draw.rect(s,(60,40,15),(bx,by,20,14),border_radius=2)
        pygame.draw.rect(s,(230,210,170),(bx+2,by+2,16,10),border_radius=1)
        pygame.draw.rect(s,(90,170,255),(bx+2,by+2,16,10),2,border_radius=1)
        self.image=s
        self.rect=self.image.get_rect(topleft=(c*TILE_SIZE,(r-2)*TILE_SIZE))
                                          
        self.hitbox=pygame.Rect(c*TILE_SIZE-TILE_SIZE//2,(r-2)*TILE_SIZE,
                                TILE_SIZE*2,TILE_SIZE*3)

class ODict(pygame.sprite.Sprite):
    def __init__(self,c,r):
        super().__init__()
        self.image=_g("dich",lambda:_khoi((240,200,20),(255,240,80),(180,140,0),"★"))
        self.rect=self.image.get_rect(topleft=(c*TILE_SIZE,r*TILE_SIZE))

class HopGo(KhucGo):
    def __init__(self,c,r):
        super().__init__(c,r); self.vel_y=0
    def update(self,ds):
        self.vel_y=min(self.vel_y+TRONG_LUC,20); self.rect.y+=int(self.vel_y)
        for n in ds:
            if self.rect.colliderect(n.rect) and self.vel_y>0:
                self.rect.bottom=n.rect.top; self.vel_y=0

ThanCay=NenTang; LaCay=NenTang

class Kiem(pygame.sprite.Sprite):
    W = TILE_SIZE
    H = TILE_SIZE * 2
    RANGE_F = TILE_SIZE * 2                        

    def __init__(self, c, r, dung=True):

        super().__init__()
        self.dung = dung
        w = TILE_SIZE if dung else TILE_SIZE*2
        h = TILE_SIZE*2 if dung else TILE_SIZE
        self.image = self._ve(w, h)
        self.rect  = self.image.get_rect(topleft=(c*TILE_SIZE, r*TILE_SIZE))
        self.hien  = True

    def _ve(self, w, h):
        s = pygame.Surface((w, h), pygame.SRCALPHA)
                       
        pygame.draw.rect(s,(255,210,20),(0,0,w,h),border_radius=6)
        pygame.draw.rect(s,(255,240,90),(2,2,w-4,h//3),border_radius=4)
                      
        if self.dung:
                           
            pygame.draw.rect(s,(220,230,255),(w//2-4,4,8,h-20))
            pygame.draw.rect(s,(240,245,255),(w//2-2,4,4,h-20))
                         
            pygame.draw.rect(s,(200,160,40),(2,h//2-4,w-4,8),border_radius=3)
                   
            pygame.draw.rect(s,(160,100,20),(w//2-5,h//2+4,10,h//3),border_radius=3)
        else:
            pygame.draw.rect(s,(220,230,255),(4,h//2-4,w-20,8))
            pygame.draw.rect(s,(200,160,40),(w//2-4,2,8,h-4),border_radius=3)
            pygame.draw.rect(s,(160,100,20),(w//2+4,h//2-5,w//3,10),border_radius=3)
              
        pygame.draw.rect(s,(180,130,0),(0,0,w,h),2,border_radius=6)
                           
        pygame.draw.circle(s,(255,255,200,180),(6,6),4)
        return s

    def co_the_nhat(self, player_rect):
        if not self.hien: return False
        return self.rect.inflate(self.RANGE_F, self.RANGE_F).colliderect(player_rect)

    def update(self, *args): pass

class KhoiDiChuyen(pygame.sprite.Sprite):
    TOC_DO = 2
    RANGE_CLICK = TILE_SIZE * 2

    def __init__(self, c, r, di_chuyen_x=True):
        super().__init__()
        self.image  = self._ve()
        self.rect   = self.image.get_rect(topleft=(c*TILE_SIZE, r*TILE_SIZE))
        self.hien   = True
                                 
        self.di_chuyen_x = di_chuyen_x
        self.vel        = self.TOC_DO
        self.goc_x      = c * TILE_SIZE
        self.goc_y      = r * TILE_SIZE
        self.bien       = TILE_SIZE * 4                  

    def _ve(self):
        s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(s,(200,60,60,230),(2,2,TILE_SIZE-4,TILE_SIZE-4),border_radius=8)
        pygame.draw.rect(s,(240,100,100,200),(4,4,TILE_SIZE-8,10),border_radius=4)
             
        pygame.draw.circle(s,(255,255,255),(14,20),5)
        pygame.draw.circle(s,(255,255,255),(34,20),5)
        pygame.draw.circle(s,(60,20,20),(15,21),3)
        pygame.draw.circle(s,(60,20,20),(35,21),3)
               
        pygame.draw.arc(s,(60,20,20),pygame.Rect(12,28,24,10),3.14,0,2)
        pygame.draw.rect(s,(160,30,30),(2,2,TILE_SIZE-4,TILE_SIZE-4),2,border_radius=8)
        return s

    def update(self, *args):
        if not self.hien: return
        if self.di_chuyen_x:
            self.rect.x += self.vel
            if abs(self.rect.x - self.goc_x) >= self.bien:
                self.vel *= -1
        else:
            self.rect.y += self.vel
            if abs(self.rect.y - self.goc_y) >= self.bien:
                self.vel *= -1

    def co_the_click(self, player_rect):
        if not self.hien: return False
        return self.rect.inflate(self.RANGE_CLICK, self.RANGE_CLICK).colliderect(player_rect)