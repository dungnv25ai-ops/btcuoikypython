# the_gioi/boss.py
import pygame, math
from cai_dat import *

T = TILE_SIZE

def _ve_boss_du_phong(mau_chinh, mau_toi):
    """Hàm này chỉ chạy nếu không tìm thấy file ảnh PNG"""
    W, H = T, T*2
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    pygame.draw.rect(s, mau_chinh, (0, 0, W, H), border_radius=6)
    pygame.draw.rect(s, mau_toi, (0, 0, W, H), 3, border_radius=6)
    return s

class Boss5(pygame.sprite.Sprite):
    """Boss màn 5 — tụ lực + bắn cầu."""
    TU_LUC_TIME = 120   
    BAN_COOLDOWN= 180   

    def __init__(self, cot, hang):
        super().__init__()
        try:
            img = pygame.image.load("tai_nguyen/hinh_anh/boss5.png").convert_alpha()
            
            # 1. CHỈNH KÍCH THƯỚC: Cho Boss to ra (ví dụ 2x2 ô cho ngầu)
            # Thay vì (T, T*2), ta dùng (T*2, T*2) để giữ dáng Boss vuông vắn
            size_moi = (T * 2, T * 2) 
            self._surf = pygame.transform.scale(img, size_moi)
            
        except:
            print("Lỗi nạp ảnh Boss")
            # Tạo khối dự phòng nếu lỗi
            self._surf = pygame.Surface((T*2, T*2)) 
            self._surf.fill((255, 0, 0))

        self.image = self._surf.copy()
        
        # 2. CHỈNH VỊ TRÍ: Để Boss đứng SÁT ĐẤT
        # Thay vì topleft, ta dùng 'midbottom' (giữa - dưới)
        # Nó sẽ đặt CHÂN của Boss vào đúng vị trí ô đất bạn đặt ký hiệu '5'
        self.rect = self.image.get_rect(midbottom=(cot * T + T//2, hang * T + T))
        
        # Các biến khác giữ nguyên...
        self._dem = 0
        self._ban_cd = self.BAN_COOLDOWN
        self._tu_luc = 0
        self.can_ban = False 

    def chuan_bi_ban(self, target_x, target_y):
        self._tu_luc = self.TU_LUC_TIME
        self._ban_sx = target_x; self._ban_sy = target_y
        self.can_ban = False

    def update(self):
        self._dem += 1
        if self._tu_luc > 0:
            self._tu_luc -= 1
            # Hiệu ứng nháy khi tụ lực (vẫn hoạt động tốt trên ảnh PNG)
            a = int(150+105*abs(math.sin(self._tu_luc*0.15)))
            f = self._surf.copy()
            f.fill((80,0,80,80), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = f; self.image.set_alpha(a)
            if self._tu_luc == 0: self.can_ban = True
        else:
            if self._ban_cd > 0: self._ban_cd -= 1
            # Hiệu ứng mờ ảo nhẹ nhàng
            a = int(200+55*abs(math.sin(self._dem*0.04)))
            self.image = self._surf.copy()
            self.image.set_alpha(a)

    def cham_nguoi(self, player_rect): return False

    def ve_thanh_thoi_gian(self, screen, cam_x, cam_y, con_lai, font):
        sx, sy = self.rect.centerx - cam_x, self.rect.top - cam_y - 24
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
    """Boss màn 10 — 10 HP."""
    SO_MAU_MAX  = 10
    TU_LUC_TIME = 90    
    BAN_COOLDOWN= 120   

    def __init__(self, cot, hang):
        super().__init__()
        try:
            img = pygame.image.load("tai_nguyen/hinh_anh/boss10.png").convert_alpha()
            size_moi = (T * 2, T * 2) 
            self._surf = pygame.transform.scale(img, size_moi)
            
        except:
            print("Lỗi nạp ảnh Boss")
            # Tạo khối dự phòng nếu lỗi
            self._surf = pygame.Surface((T*2, T*2)) 
            self._surf.fill((255, 0, 0))

        self.image = self._surf.copy()
        self.rect = self.image.get_rect(midbottom=(cot * T + T//2, hang * T + T))
        
        # Các biến khác giữ nguyên...
        self._dem = 0
        self._ban_cd = self.BAN_COOLDOWN
        self._tu_luc = 0
        self.can_ban = False
    def nhan_don(self):
        if self.mau <= 0: return True
        self.mau -= 1
        self._flash = 14
        return self.mau <= 0

    def da_chet(self): return self.mau <= 0
    def cham_nguoi(self, player_rect): return False

    def update(self):
        self._dem += 1
        # 1. Xử lý tụ lực
        if self._tu_luc > 0 and not self.da_chet():
            self._tu_luc -= 1
            a = int(150+105*abs(math.sin(self._tu_luc*0.2)))
            f = self._surf.copy()
            f.fill((80,0,0,100), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = f; self.image.set_alpha(a)
            if self._tu_luc == 0: self.can_ban = True
            return
        
        if not self.da_chet() and self._ban_cd > 0: self._ban_cd -= 1
        
        # 2. Hiệu ứng chết (mờ dần)
        if self.da_chet():
            cur = self.image.get_alpha() or 255
            self.image.set_alpha(max(0, cur-8))
            if cur <= 8: self.kill()
            return
            
        # 3. Hiệu ứng bị chém (nháy trắng) hoặc thở bình thường
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
        sx, sy = self.rect.centerx - cam_x, self.rect.top - cam_y - 24
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