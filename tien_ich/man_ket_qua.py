# tien_ich/man_ket_qua.py
import pygame, math
from cai_dat import *


class ManKetQua:
    def __init__(self):
        self.hien   = False
        self.thang  = False
        self.so_sao = 0
        self.so_man = 1
        self._dem   = 0
        self.ft = self.fm = self.fn = None

    def _init_font(self, h):
        if not self.ft:
            self.ft = pygame.font.SysFont(FONT_CHINH, max(36,h//11), bold=True)
            self.fm = pygame.font.SysFont(FONT_CHINH, max(20,h//18), bold=True)
            self.fn = pygame.font.SysFont(FONT_CHINH, max(15,h//28))

    def hien_thang(self, so_man, so_sao):
        self.hien=True; self.thang=True
        self.so_man=so_man; self.so_sao=so_sao; self._dem=0

    def hien_thua(self, so_man):
        self.hien=True; self.thang=False
        self.so_man=so_man; self._dem=0

    def an(self):
        self.hien = False

    # ── Lấy danh sách nút theo trạng thái ─────────────────
    def _lay_labels(self):
        if self.thang:
            labs = [("Choi lai","choi_lai")]
            if self.so_man < 10:
                labs.append((f"Man {self.so_man+1}","man_tiep"))
            labs.append(("Man chinh","man_chinh"))
        else:
            labs = [("Choi lai","choi_lai"),("Man chinh","man_chinh")]
        return labs

    # ── Tính rect các nút (dùng chung cho vẽ và click) ────
    def _tinh_nut(self, w, h):
        BW = min(460,w-40); BH = min(300,h-60)
        bx = (w-BW)//2;     by = (h-BH)//2
        labels = self._lay_labels()
        n  = len(labels); NW=120; NH=40; GAP=14
        tw = n*NW+(n-1)*GAP
        nx0= bx+(BW-tw)//2; ny=by+BH-NH-20
        rects = {}
        for i,(nhan,key) in enumerate(labels):
            rects[key] = pygame.Rect(nx0+i*(NW+GAP), ny, NW, NH)
        return bx,by,BW,BH, rects

    # ── Vẽ ────────────────────────────────────────────────
    def ve(self, screen):
        if not self.hien: return
        w,h = screen.get_size()
        self._init_font(h); self._dem+=1

        ov = pygame.Surface((w,h),pygame.SRCALPHA)
        ov.fill((0,0,0,175)); screen.blit(ov,(0,0))

        bx,by,BW,BH,rects = self._tinh_nut(w,h)
        mau_k = (10,30,10) if self.thang else (30,10,10)
        mau_v = (50,200,100) if self.thang else (200,50,50)
        pygame.draw.rect(screen,mau_k,(bx,by,BW,BH),border_radius=14)
        pygame.draw.rect(screen,mau_v,(bx,by,BW,BH),3,border_radius=14)

        if self.thang:
            t1 = self.ft.render("THANG ROI!",True,VANG)
            screen.blit(t1,t1.get_rect(center=(bx+BW//2,by+38)))
            # Sao
            R=18; sx0=bx+BW//2-3*(R*2+10)//2
            for i in range(3):
                cx=sx0+i*(R*2+10)+R; cy=by+95
                cy+=int(4*math.sin(self._dem*0.05+i))
                pts=[]
                for j in range(10):
                    a=math.radians(-90+j*36); ri=R if j%2==0 else R//2
                    pts.append((cx+ri*math.cos(a),cy+ri*math.sin(a)))
                mau=(255,215,0) if i<self.so_sao else (60,55,20)
                pygame.draw.polygon(screen,mau,pts)
                if i<self.so_sao:
                    pygame.draw.polygon(screen,(255,255,150),pts,2)
            t2=self.fn.render(f"Da thu thap {self.so_sao}/3 ngoi sao",True,TRANG)
            screen.blit(t2,t2.get_rect(center=(bx+BW//2,by+148)))
        else:
            t1=self.ft.render("GAME OVER",True,(220,60,60))
            t2=self.fn.render("Ban da mat het mang!",True,(200,150,150))
            screen.blit(t1,t1.get_rect(center=(bx+BW//2,by+55)))
            screen.blit(t2,t2.get_rect(center=(bx+BW//2,by+108)))

        # Nút
        mx,my = pygame.mouse.get_pos()
        labels = self._lay_labels()
        for nhan,key in labels:
            r = rects[key]
            hv= r.collidepoint(mx,my)
            if   key=="choi_lai":  mc=(50,130,50) if not hv else (70,180,70)
            elif key=="man_tiep":  mc=(50,80,150) if not hv else (70,120,200)
            else:                  mc=(80,80,120) if not hv else (110,110,170)
            pygame.draw.rect(screen,mc,r,border_radius=8)
            pygame.draw.rect(screen,(160,160,210),r,1,border_radius=8)
            t=self.fn.render(nhan,True,TRANG)
            screen.blit(t,t.get_rect(center=r.center))

    # ── Xử lý click ───────────────────────────────────────
    def xu_ly_click(self, pos, w, h):
        """Trả về 'choi_lai','man_tiep','man_chinh' hoặc None."""
        if not self.hien: return None
        _,_,_,_, rects = self._tinh_nut(w, h)
        for key,r in rects.items():
            if r.collidepoint(pos):
                return key
        return None
