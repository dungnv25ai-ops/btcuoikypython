# the_gioi/boss.py — Boss đứng yên 1x2
import pygame, math
from cai_dat import *

T = TILE_SIZE

def _ve_boss(mau_chinh, mau_sang, mau_toi, ky="B"):
    W, H = T, T*2
    s = pygame.Surface((W,H), pygame.SRCALPHA)
    pygame.draw.rect(s, mau_chinh, (0,0,W,H), border_radius=6)
    pygame.draw.rect(s, mau_sang,  (2,2,W-4,H//2), border_radius=5)
    pygame.draw.rect(s, mau_toi,   (2,H//2,W-4,H//2-2), border_radius=5)
    # Mắt
    for ey in [H//4, H*3//4]:
        pygame.draw.circle(s,(255,50,50),(W//2-8,ey),6)
        pygame.draw.circle(s,(255,50,50),(W//2+8,ey),6)
        pygame.draw.circle(s,(255,200,0),(W//2-8,ey),3)
        pygame.draw.circle(s,(255,200,0),(W//2+8,ey),3)
    # Viền
    pygame.draw.rect(s, mau_toi, (0,0,W,H), 2, border_radius=6)
    return s


class Boss5(pygame.sprite.Sprite):
    """Boss màn 5 — tụ lực + bắn cầu. Sống sót 60s thắng."""
    TU_LUC_TIME = 120   # 2s tụ lực
    BAN_COOLDOWN= 180   # 3s giữa các lần bắn

    def __init__(self, cot, hang):
        super().__init__()
        self._surf = _ve_boss((140,20,160),(180,50,200),(90,10,110))
        self.image = self._surf.copy()
        self.rect  = self.image.get_rect(topleft=(cot*T, hang*T))
        self._dem     = 0
        self._ban_cd  = self.BAN_COOLDOWN
        self._tu_luc  = 0    # đang tụ lực (đếm xuống)
        self._ban_sx  = 0    # tọa độ target khi bắn
        self._ban_sy  = 0
        self.can_ban  = False  # có quả cầu cần bắn không

    def chuan_bi_ban(self, target_x, target_y):
        """Gọi từ man_choi khi cooldown hết."""
        self._tu_luc = self.TU_LUC_TIME
        self._ban_sx = target_x
        self._ban_sy = target_y
        self.can_ban = False

    def update(self):
        self._dem += 1
        if self._tu_luc > 0:
            self._tu_luc -= 1
            # Flash khi tụ lực
            a = int(150+105*abs(math.sin(self._tu_luc*0.15)))
            f = self._surf.copy()
            f.fill((80,0,80,80), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = f; self.image.set_alpha(a)
            if self._tu_luc == 0:
                self.can_ban = True   # xong tụ lực → bắn
        else:
            if self._ban_cd > 0: self._ban_cd -= 1
            a = int(200+55*abs(math.sin(self._dem*0.04)))
            self.image = self._surf.copy()
            self.image.set_alpha(a)

    def cham_nguoi(self, player_rect):
        return False

    def ve_thanh_thoi_gian(self, screen, cam_x, cam_y, con_lai, font):
        sx = self.rect.centerx - cam_x
        sy = self.rect.top     - cam_y - 24
        BW, BH = 120, 12
        bx = sx - BW//2
        pygame.draw.rect(screen,(30,30,30),(bx,sy,BW,BH),border_radius=5)
        tl = max(0, con_lai/60)
        mau = (50,200,50) if tl>0.4 else (220,160,0) if tl>0.2 else (220,50,50)
        pygame.draw.rect(screen,mau,(bx,sy,int(BW*tl),BH),border_radius=5)
        pygame.draw.rect(screen,(180,180,180),(bx,sy,BW,BH),1,border_radius=5)
        t = font.render(f"{int(con_lai)}s", True, TRANG)
        screen.blit(t, t.get_rect(center=(sx, sy-12)))


class Boss10(pygame.sprite.Sprite):
    """Boss màn 10 — tụ lực + bắn cầu. 5 HP, kill trong 60s thắng."""
    SO_MAU_MAX  = 10
    TU_LUC_TIME = 90    # 1.5s tụ lực
    BAN_COOLDOWN= 120   # 2s giữa các lần bắn

    def __init__(self, cot, hang):
        super().__init__()
        self._surf = _ve_boss((160,20,20),(200,50,50),(100,10,10))
        self.image = self._surf.copy()
        self.rect  = self.image.get_rect(topleft=(cot*T, hang*T))
        self._dem    = 0
        self.mau     = self.SO_MAU_MAX
        self._flash  = 0
        self._ban_cd = self.BAN_COOLDOWN
        self._tu_luc = 0
        self._ban_sx = 0; self._ban_sy = 0
        self.can_ban = False

    def chuan_bi_ban(self, target_x, target_y):
        self._tu_luc = self.TU_LUC_TIME
        self._ban_sx = target_x; self._ban_sy = target_y
        self.can_ban = False

    def nhan_don(self):
        """Chém -1 máu. Trả về True nếu chết."""
        if self.mau <= 0: return True
        self.mau -= 1
        self._flash = 14
        return self.mau <= 0

    def da_chet(self):
        return self.mau <= 0

    def cham_nguoi(self, player_rect):
        return False   # không tấn công

    def update(self):
        self._dem += 1
        if self._tu_luc > 0 and not self.da_chet():
            self._tu_luc -= 1
            a = int(150+105*abs(math.sin(self._tu_luc*0.2)))
            f = self._surf.copy()
            f.fill((80,0,0,100), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = f; self.image.set_alpha(a)
            if self._tu_luc == 0: self.can_ban = True
            return
        if not self.da_chet() and self._ban_cd > 0: self._ban_cd -= 1
        if self.da_chet():
            cur = self.image.get_alpha() or 255
            self.image.set_alpha(max(0, cur-8))
            if cur <= 8: self.kill()
            return
        if self._flash > 0:
            self._flash -= 1
            f = self._surf.copy()
            f.fill((255,255,255,140), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = f
        else:
            a = int(200+55*abs(math.sin(self._dem*0.04)))
            self.image = self._surf.copy()
            self.image.set_alpha(a)

    def ve_thanh_mau(self, screen, cam_x, cam_y, font):
        if self.da_chet(): return
        sx = self.rect.centerx - cam_x
        sy = self.rect.top     - cam_y - 24
        BW, BH = 130, 14
        bx = sx - BW//2
        pygame.draw.rect(screen,(40,10,10),(bx,sy,BW,BH),border_radius=5)
        tl = self.mau / self.SO_MAU_MAX
        pygame.draw.rect(screen,(200,30,30),(bx,sy,int(BW*tl),BH),border_radius=5)
        pygame.draw.rect(screen,(220,150,150),(bx,sy,BW,BH),1,border_radius=5)
        for i in range(1, self.SO_MAU_MAX):
            vx = bx + int(BW*i/self.SO_MAU_MAX)
            pygame.draw.line(screen,(0,0,0),(vx,sy),(vx,sy+BH),2)
        t = font.render(f"BOSS {self.mau}/{self.SO_MAU_MAX}", True, TRANG)
        screen.blit(t, t.get_rect(center=(sx, sy-12)))
