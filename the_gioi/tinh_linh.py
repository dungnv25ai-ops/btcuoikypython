# the_gioi/tinh_linh.py
import pygame, math, time
from cai_dat import *

S = TILE_SIZE

def _ve():
    surf = pygame.Surface((S, S), pygame.SRCALPHA)
    pygame.draw.rect(surf,(100,200,255,200),(4,4,S-8,S-8),border_radius=8)
    pygame.draw.rect(surf,(200,240,255,230),(6,6,S-12,S-12),border_radius=6)
    pygame.draw.rect(surf,(255,255,255,200),(10,10,S-20,S-20),border_radius=4)
    pygame.draw.rect(surf,(150,220,255,255),(4,4,S-8,S-8),2,border_radius=8)
    pygame.draw.circle(surf,(255,255,255,255),(S//2,S//2),4)
    return surf

_SPRITE = None
def _get():
    global _SPRITE
    if _SPRITE is None: _SPRITE = _ve()
    return _SPRITE


def _di_chuyen_khong_xuyen(x, y, mx, my, size, ds_nen):
    """Di chuyển (mx,my) có collision trượt — dùng chung cho tinh linh."""
    if not ds_nen:
        return x + mx, y + my

    # Ngang trước
    nx = x + mx
    r  = pygame.Rect(int(nx), int(y), size, size)
    for n in ds_nen:
        if r.colliderect(n.rect):
            if mx > 0: nx = float(n.rect.left - size)
            elif mx < 0: nx = float(n.rect.right)
            mx = 0; break

    # Dọc sau
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
        # Hội thoại trigger
        self.cau_thoai    = ""
        self.dang_noi     = False
        self.thoi_gian_bat= 0.0
        self.thoi_luong   = 5.0
        self.trigger_x    = None
        self.da_trigger   = False
        self.font_thoai   = self.font_ten = None
        # Double-click → platform
        self._click_t    = 0.0
        self._click_pos  = None
        self.DOUBLE_T    = 0.45
        self.DOUBLE_R    = 100
        # Platform state
        self.la_platform       = False
        self._dang_di_chuyen   = False
        self._dich_x = self._dich_y = 0.0
        self._thoi_gian_dung   = 0.0
        self.PLATFORM_TIME     = 10.0   # giây đứng yên

    # ── Rect va chạm 1x1 khi là platform ─────────────────
    @property
    def rect(self):
        if self.la_platform or self._dang_di_chuyen:
            return pygame.Rect(int(self.x), int(self.y), S, S)
        return None

    def bat_dau(self, x, y):
        self.x, self.y = float(x), float(y)
        self.hien = True

    def dat_trigger(self, world_x, cau):
        self.trigger_x  = world_x
        self.cau_thoai  = cau
        self.da_trigger = False

    def kich_hoat_thoai(self):
        self.dang_noi     = True
        self.thoi_gian_bat= time.time()

    # ── Double-click ──────────────────────────────────────
    def xu_ly_click(self, world_x, world_y):
        now = time.time()
        if (self._click_t > 0
                and now - self._click_t <= self.DOUBLE_T
                and self._click_pos is not None
                and math.hypot(world_x-self._click_pos[0],
                               world_y-self._click_pos[1]) <= self.DOUBLE_R):
            self._click_t   = 0.0
            self._click_pos = None
            self._bay_toi(world_x, world_y)
            return True
        self._click_t   = now
        self._click_pos = (world_x, world_y)
        return False

    def _bay_toi(self, wx, wy):
        # Điều chỉnh đích để rect 1x1 nằm đúng chỗ click (căn giữa)
        self._dich_x        = float(wx) - S//2
        self._dich_y        = float(wy) - S//2
        self._dang_di_chuyen= True
        self.la_platform    = False

    # ── Update ───────────────────────────────────────────
    def update(self, player_rect, ds_nen=None):
        if not self.hien: return
        self.dem += 1; self.quy_dao += 0.025

        # Trigger thoại
        if self.trigger_x and not self.da_trigger \
                and player_rect.centerx >= self.trigger_x:
            self.da_trigger = True; self.kich_hoat_thoai()
        if self.dang_noi and time.time()-self.thoi_gian_bat >= self.thoi_luong:
            self.dang_noi = False

        if self._dang_di_chuyen:
            dx = self._dich_x - self.x
            dy = self._dich_y - self.y
            dist = math.hypot(dx, dy)
            if dist < 6:
                self.x, self.y       = self._dich_x, self._dich_y
                self._dang_di_chuyen = False
                self.la_platform     = True
                self._thoi_gian_dung = time.time()
            else:
                spd = min(14, max(4, dist*0.18))
                mx  = dx/dist*spd
                my  = dy/dist*spd
                self.x, self.y = _di_chuyen_khong_xuyen(
                    self.x, self.y, mx, my, S, ds_nen)

        elif self.la_platform:
            if time.time() - self._thoi_gian_dung >= self.PLATFORM_TIME:
                self.la_platform = False

        else:
            # Bay quanh nhân vật — áp trượt nhẹ
            cx = player_rect.centerx + math.cos(self.quy_dao)*55
            cy = player_rect.top - 12 + math.sin(self.quy_dao*1.3)*16
            mx = (cx-self.x)*0.06
            my = (cy-self.y)*0.06
            self.x, self.y = _di_chuyen_khong_xuyen(
                self.x, self.y, mx, my, S, ds_nen)

    def ve(self, screen, cam_x, cam_y, mw, mh):
        if not self.hien: return
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)
        # Glow
        alpha = int(40+25*math.sin(self.dem*0.07))
        rg    = int(28+6*math.sin(self.dem*0.05))
        g = pygame.Surface((rg*2,rg*2),pygame.SRCALPHA)
        pygame.draw.circle(g,(80,200,255,alpha),(rg,rg),rg)
        screen.blit(g,(sx-rg+S//2,sy-rg+S//2))
        screen.blit(_get(),(sx,sy))
        # Viền vàng khi là platform + đếm ngược
        if self.la_platform:
            pygame.draw.rect(screen,VANG,(sx,sy,S,S),3,border_radius=6)
            con_lai = max(0.0, self.PLATFORM_TIME-(time.time()-self._thoi_gian_dung))
            if not self.font_thoai:
                self.font_thoai = pygame.font.SysFont(FONT_CHINH,16)
            t = self.font_thoai.render(f"{con_lai:.1f}s",True,VANG)
            screen.blit(t,(sx,sy-18))
        if self.dang_noi: self._ve_bong(screen,sx,sy,mw,mh)

    def _ve_bong(self,screen,sx,sy,mw,mh):
        if not self.font_thoai:
            self.font_thoai=pygame.font.SysFont(FONT_CHINH,16)
            self.font_ten  =pygame.font.SysFont(FONT_CHINH,14,bold=True)
        if not self.cau_thoai: return
        tl=time.time()-self.thoi_gian_bat; prog=min(1.0,tl/self.thoi_luong)
        lines=self._ngat(self.cau_thoai,240)
        PAD,BW=12,280; BH=len(lines)*20+PAD*2+30
        bx=max(8,min(sx-BW//2,mw-BW-8)); by=max(8,sy-BH-16)
        bong=pygame.Surface((BW,BH),pygame.SRCALPHA)
        pygame.draw.rect(bong,(238,246,255,235),(0,0,BW,BH),border_radius=10)
        pygame.draw.rect(bong,(90,170,255,255),(0,0,BW,BH),2,border_radius=10)
        screen.blit(bong,(bx,by))
        tip=sx+S//2
        pygame.draw.polygon(screen,(238,246,255),[(tip-7,by+BH),(tip+7,by+BH),(tip,by+BH+10)])
        pygame.draw.polygon(screen,(90,170,255),[(tip-7,by+BH),(tip+7,by+BH),(tip,by+BH+10)],1)
        screen.blit(self.font_ten.render("Tinh Linh",True,(50,120,210)),(bx+PAD,by+PAD))
        for i,d in enumerate(lines):
            screen.blit(self.font_thoai.render(d,True,(25,25,45)),(bx+PAD,by+PAD+19+i*20))
        bar_y=by+BH-10
        pygame.draw.rect(screen,(180,200,230),(bx+PAD,bar_y,BW-PAD*2,6),border_radius=3)
        pw=int((BW-PAD*2)*(1-prog))
        pygame.draw.rect(screen,(60,140,220),(bx+PAD,bar_y,pw,6),border_radius=3)

    def _ngat(self,text,max_w):
        if not self.font_thoai: return [text]
        words,lines,cur=text.split(),[],""
        for w in words:
            t=(cur+" "+w).strip()
            if self.font_thoai.size(t)[0]<=max_w: cur=t
            else:
                if cur: lines.append(cur); cur=w
        if cur: lines.append(cur)
        return lines or [""]
