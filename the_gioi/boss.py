                  
import pygame, math, os as _os
from cai_dat import *

T = TILE_SIZE

_THU_MUC_GD = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))

_CACHE_VK = {}                                 

def _load_vu_khi(path_rel):

    if path_rel in _CACHE_VK:
        return _CACHE_VK[path_rel]
    full = _os.path.join(_THU_MUC_GD, *path_rel.split("/"))
    try:
        img  = pygame.image.load(full).convert_alpha()
        img  = pygame.transform.scale(img, (T, T * 2))
        flip = pygame.transform.flip(img, True, False)
        _CACHE_VK[path_rel] = (img, flip)
        return img, flip
    except Exception:
                                          
        s = pygame.Surface((T, T * 2), pygame.SRCALPHA)
        pygame.draw.rect(s, (220, 200, 30), (T//3, 0, T//3, T*2), border_radius=4)
        pygame.draw.rect(s, (180, 140, 0),  (T//3, 0, T//3, T*2), 2, border_radius=4)
        f = pygame.transform.flip(s, True, False)
        _CACHE_VK[path_rel] = (s, f)
        return s, f

class Boss5(pygame.sprite.Sprite):

    TU_LUC_TIME = 120   
    BAN_COOLDOWN= 180
    TRONG_LUC   = 0.8
    TOC_DO_ROI_MAX = 18
   
    def __init__(self, cot, hang):
        super().__init__()
        try:
            path = _os.path.join(_THU_MUC_GD, "tai_nguyen", "hinh_anh", "boss5.png")
            img = pygame.image.load(path).convert_alpha()
            size_moi = (T * 2, T * 2) 
            self._surf = pygame.transform.scale(img, size_moi)
        except Exception as e:
            print("Lỗi nạp ảnh Boss5:", e)
            self._surf = pygame.Surface((T*2, T*2), pygame.SRCALPHA)
            self._surf.fill((255, 0, 0))

        self.image = self._surf.copy()
        self._surf_flip = pygame.transform.flip(self._surf, True, False)
        self._flip = False
        self.rect = self.image.get_rect(midbottom=(cot * T + T//2, hang * T + T))

        anh_gay_goc, _ = _load_vu_khi("tai_nguyen/hinh_anh/gay.png")
    
        w_goc, h_goc = anh_gay_goc.get_size()
        ty_le = w_goc / h_goc
    
        chieu_cao = int(T * 1.5) 

        chieu_rong = int(chieu_cao * ty_le) 
        
        self._vk = pygame.transform.scale(anh_gay_goc, (chieu_rong, chieu_cao))
        self._vk_flip = pygame.transform.flip(self._vk, True, False)

        self._dem = 0
        self._ban_cd = self.BAN_COOLDOWN
        self._tu_luc = 0
        self.can_ban = False
                            
        self.vel_y      = 0.0
        self._khoa_vi_tri = False                                                     

    def _anh_goc(self):

        return self._surf_flip if self._flip else self._surf

    def quay_ve(self, player_x):

        self._flip = player_x > self.rect.centerx
        
    def chuan_bi_ban(self, target_x, target_y):
        self._tu_luc = self.TU_LUC_TIME
        self._ban_sx = target_x; self._ban_sy = target_y
        self.can_ban = False
    def khoa_giua_map(self, map_w, map_h):

        self._khoa_vi_tri = True
        self.vel_y = 0.0
        self.rect.center = (map_w // 2, map_h // 2)

    def mo_khoa_vi_tri(self):

        self._khoa_vi_tri = False

    def ap_dung_vat_ly(self, ds_nen):

        if self._khoa_vi_tri:
            return
        self.vel_y = min(self.vel_y + self.TRONG_LUC, self.TOC_DO_ROI_MAX)
        self.rect.y += int(self.vel_y)
        for n in ds_nen:
            if self.rect.colliderect(n.rect) and self.vel_y > 0:
                self.rect.bottom = n.rect.top
                self.vel_y = 0
                break

    def update(self):
        self._dem += 1
        anh_goc = self._anh_goc()
        if self._tu_luc > 0:
            self._tu_luc -= 1
                                                                       
            a = int(150+105*abs(math.sin(self._tu_luc*0.15)))
            f = anh_goc.copy()
            f.fill((80,0,80,80), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = f; self.image.set_alpha(a)
            if self._tu_luc == 0: self.can_ban = True
        else:
            if self._ban_cd > 0: self._ban_cd -= 1
                                      
            a = int(200+55*abs(math.sin(self._dem*0.04)))
            self.image = anh_goc.copy()
            self.image.set_alpha(a)

    def cham_nguoi(self, player_rect): return False

    def ve_vu_khi(self, screen, cam_x, cam_y):

        anh = self._vk_flip if self._flip else self._vk
        
        if self._flip:
                                                    
            x = self.rect.right - (T // 1.5) - cam_x
        else:
                                                         
            x = self.rect.left - (T // 4) - cam_x +10

        y = self.rect.centery - (T // 3) - cam_y - 20
        
        screen.blit(anh, (x, y))

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

    SO_MAU_MAX  = 10
    TU_LUC_TIME = 90    
    BAN_COOLDOWN= 120  
    TRONG_LUC   = 0.8
    TOC_DO_ROI_MAX = 18
 
    def __init__(self, cot, hang):
        super().__init__()
        try:
            path = _os.path.join(_THU_MUC_GD, "tai_nguyen", "hinh_anh", "boss10.png")
            img = pygame.image.load(path).convert_alpha()
            size_moi = (T * 2, T * 2) 
            self._surf = pygame.transform.scale(img, size_moi)
        except Exception as e:
            print("Lỗi nạp ảnh Boss10:", e)
            self._surf = pygame.Surface((T*2, T*2), pygame.SRCALPHA)
            self._surf.fill((255, 0, 0))

        self.image = self._surf.copy()
        self._surf_flip = pygame.transform.flip(self._surf, True, False)
        self._flip = False
        self.rect = self.image.get_rect(midbottom=(cot * T + T//2, hang * T + T))

        anh_kiem_goc, _ = _load_vu_khi("tai_nguyen/hinh_anh/nhan_vat/kiem.png")
        
        KICH_THUOC_KIEM_BOSS = (int(T ), int(T ))
        kiem_resize = pygame.transform.scale(anh_kiem_goc, KICH_THUOC_KIEM_BOSS)
        
        self._vk = pygame.transform.rotate(kiem_resize, -135)
        
        self._vk_flip = pygame.transform.flip(self._vk, True, False)
                                                                    
        self._dem = 0
        self._ban_cd = self.BAN_COOLDOWN
        self._tu_luc = 0
        self.can_ban = False
        self.mau     = self.SO_MAU_MAX
        self._flash  = 0
                        
        self.vel_y         = 0.0
        self._khoa_vi_tri  = False                                                     

    def khoa_giua_map(self, map_w, map_h):

        self._khoa_vi_tri = True
        self.vel_y = 0.0
        self.rect.center = (map_w // 2, map_h // 2)

    def mo_khoa_vi_tri(self):

        self._khoa_vi_tri = False

    def ap_dung_vat_ly(self, ds_nen):

        if self._khoa_vi_tri or self.da_chet():
            return
        self.vel_y = min(self.vel_y + self.TRONG_LUC, self.TOC_DO_ROI_MAX)
        self.rect.y += int(self.vel_y)
        for n in ds_nen:
            if self.rect.colliderect(n.rect) and self.vel_y > 0:
                self.rect.bottom = n.rect.top
                self.vel_y = 0
                break

    def _anh_goc(self):
        return self._surf_flip if self._flip else self._surf

    def quay_ve(self, player_x):

        self._flip = player_x > self.rect.centerx

    def nhan_don(self):
        if self.mau <= 0: return True
        self.mau -= 1
        self._flash = 14
        return self.mau <= 0

    def da_chet(self): return self.mau <= 0
    def cham_nguoi(self, player_rect): return False

    def ve_vu_khi(self, screen, cam_x, cam_y):

        anh = self._vk_flip if self._flip else self._vk
        
        if self._flip:
                                                             
            x = self.rect.right - (T // 1.5) - cam_x
        else:
                                                                 
            x = self.rect.left - (T // 4) - cam_x - 20

        y = self.rect.centery - (T // 3) - cam_y - 30
        
        screen.blit(anh, (x, y))

    def update(self):
        self._dem += 1
        anh_goc = self._anh_goc()
                         
        if self._tu_luc > 0 and not self.da_chet():
            self._tu_luc -= 1
            a = int(150+105*abs(math.sin(self._tu_luc*0.2)))
            f = anh_goc.copy()
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
            f = anh_goc.copy()
            f.fill((255,255,255,140), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = f
        else:
            a = int(200+55*abs(math.sin(self._dem*0.04)))
            self.image = anh_goc.copy()
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