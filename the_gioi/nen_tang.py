# the_gioi/nen_tang.py
import pygame
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

class NenTang(pygame.sprite.Sprite):
    def __init__(self,c,r):
        super().__init__()
        self.image=_g("dat",lambda:_khoi((70,150,40),(100,190,60),(45,110,25)))
        self.rect=self.image.get_rect(topleft=(c*TILE_SIZE,r*TILE_SIZE))

class NenTangBoss(pygame.sprite.Sprite):
    def __init__(self,c,r):
        super().__init__()
        self.image=_g("boss",lambda:_khoi((70,70,85),(100,100,120),(40,40,55)))
        self.rect=self.image.get_rect(topleft=(c*TILE_SIZE,r*TILE_SIZE))

class KhucGo(pygame.sprite.Sprite):
    def __init__(self,c,r):
        super().__init__()
        self.image=_g("go",lambda:_khoi((150,95,35),(195,135,65),(105,60,18),"W"))
        self.rect=self.image.get_rect(topleft=(c*TILE_SIZE,r*TILE_SIZE))

class Sach(pygame.sprite.Sprite):
    """Sách bám vào tường — W/S để trèo."""
    def __init__(self,c,r):
        super().__init__()
        s=pygame.Surface((TILE_SIZE,TILE_SIZE*3),pygame.SRCALPHA)
        # Trụ leo (dây leo)
        pygame.draw.rect(s,(100,80,40),(TILE_SIZE//2-4,0,8,TILE_SIZE*3))
        pygame.draw.rect(s,(130,105,55),(TILE_SIZE//2-3,0,3,TILE_SIZE*3))
        # Nấc leo mỗi TILE_SIZE
        for y in [TILE_SIZE//2, TILE_SIZE+TILE_SIZE//2, TILE_SIZE*2+TILE_SIZE//2]:
            pygame.draw.rect(s,(160,120,60),(TILE_SIZE//2-14,y-4,28,8),border_radius=3)
            pygame.draw.rect(s,(190,150,80),(TILE_SIZE//2-13,y-3,26,3))
        # Icon sách nhỏ ở giữa
        bx,by=TILE_SIZE//2-10,TILE_SIZE-10
        pygame.draw.rect(s,(60,40,15),(bx,by,20,14),border_radius=2)
        pygame.draw.rect(s,(230,210,170),(bx+2,by+2,16,10),border_radius=1)
        pygame.draw.rect(s,(90,170,255),(bx+2,by+2,16,10),2,border_radius=1)
        self.image=s
        self.rect=self.image.get_rect(topleft=(c*TILE_SIZE,(r-2)*TILE_SIZE))
        # Vùng tương tác (hitbox rộng hơn)
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

# ── Kiếm 1x2 (vật phẩm đặc biệt) ─────────────────────────
class Kiem(pygame.sprite.Sprite):
    W = TILE_SIZE
    H = TILE_SIZE * 2
    RANGE_F = TILE_SIZE * 2   # khoảng cách để nhặt

    def __init__(self, c, r, dung=True):
        """dung=True: dựng đứng (1x2 dọc), False: nằm ngang (2x1)"""
        super().__init__()
        self.dung = dung
        w = TILE_SIZE if dung else TILE_SIZE*2
        h = TILE_SIZE*2 if dung else TILE_SIZE
        self.image = self._ve(w, h)
        self.rect  = self.image.get_rect(topleft=(c*TILE_SIZE, r*TILE_SIZE))
        self.hien  = True

    def _ve(self, w, h):
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        # Nền vàng sáng
        pygame.draw.rect(s,(255,210,20),(0,0,w,h),border_radius=6)
        pygame.draw.rect(s,(255,240,90),(2,2,w-4,h//3),border_radius=4)
        # Hoa văn kiếm
        if self.dung:
            # Lưỡi kiếm dọc
            pygame.draw.rect(s,(220,230,255),(w//2-4,4,8,h-20))
            pygame.draw.rect(s,(240,245,255),(w//2-2,4,4,h-20))
            # Guard ngang
            pygame.draw.rect(s,(200,160,40),(2,h//2-4,w-4,8),border_radius=3)
            # Chuôi
            pygame.draw.rect(s,(160,100,20),(w//2-5,h//2+4,10,h//3),border_radius=3)
        else:
            pygame.draw.rect(s,(220,230,255),(4,h//2-4,w-20,8))
            pygame.draw.rect(s,(200,160,40),(w//2-4,2,8,h-4),border_radius=3)
            pygame.draw.rect(s,(160,100,20),(w//2+4,h//2-5,w//3,10),border_radius=3)
        # Viền
        pygame.draw.rect(s,(180,130,0),(0,0,w,h),2,border_radius=6)
        # Hiệu ứng lấp lánh
        pygame.draw.circle(s,(255,255,200,180),(6,6),4)
        return s

    def co_the_nhat(self, player_rect):
        if not self.hien: return False
        return self.rect.inflate(self.RANGE_F, self.RANGE_F).colliderect(player_rect)

    def update(self, *args): pass


# ── Khối di chuyển 1x1 ────────────────────────────────────
class KhoiDiChuyen(pygame.sprite.Sprite):
    TOC_DO = 2
    RANGE_CLICK = TILE_SIZE * 2

    def __init__(self, c, r, di_chuyen_x=True):
        super().__init__()
        self.image  = self._ve()
        self.rect   = self.image.get_rect(topleft=(c*TILE_SIZE, r*TILE_SIZE))
        self.hien   = True
        # Tuần tra ngang hoặc dọc
        self.di_chuyen_x = di_chuyen_x
        self.vel        = self.TOC_DO
        self.goc_x      = c * TILE_SIZE
        self.goc_y      = r * TILE_SIZE
        self.bien       = TILE_SIZE * 4   # biên tuần tra

    def _ve(self):
        s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(s,(200,60,60,230),(2,2,TILE_SIZE-4,TILE_SIZE-4),border_radius=8)
        pygame.draw.rect(s,(240,100,100,200),(4,4,TILE_SIZE-8,10),border_radius=4)
        # Mắt
        pygame.draw.circle(s,(255,255,255),(14,20),5)
        pygame.draw.circle(s,(255,255,255),(34,20),5)
        pygame.draw.circle(s,(60,20,20),(15,21),3)
        pygame.draw.circle(s,(60,20,20),(35,21),3)
        # Miệng
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
