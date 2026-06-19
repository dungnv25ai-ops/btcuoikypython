                                                              
import pygame
from cai_dat import *
from the_gioi.tinh_linh import load_bo_anh_tinh_linh, _di_chuyen_khong_xuyen, S

class TinhLinhDieuKhien:

    TOC_DO = 5

    def __init__(self, x, y):
                                  
        self.x = float(x)
        self.y = float(y)
        self.data_anh = load_bo_anh_tinh_linh() 
        
        self.trang_thai = "DUNG_TRAI"  
        self._dem_action = 0      
        
        self.image = self.data_anh[0]
        self.rect = pygame.Rect(int(x), int(y), S, S)

    def update(self, ds_nen=None):

        p = pygame.key.get_pressed()
        mx = my = 0

        if p[pygame.K_LEFT] or p[pygame.K_a]:
            mx -= self.TOC_DO
        if p[pygame.K_RIGHT] or p[pygame.K_d]:
            mx += self.TOC_DO
        if p[pygame.K_UP] or p[pygame.K_w]: 
            my -= self.TOC_DO
        if p[pygame.K_DOWN] or p[pygame.K_s]: 
            my += self.TOC_DO

        trang_thai_moi = self.trang_thai

        if mx < 0:
            trang_thai_moi = "BAY_TRAI"                         
        elif mx > 0:
            trang_thai_moi = "BAY_PHAI"                          
        elif my != 0:
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

        self._dem_action += 1
        
        self.image = self.data_anh[idx]

        self.x, self.y = _di_chuyen_khong_xuyen(self.x, self.y, mx, my, S, ds_nen)
        self.rect.topleft = (int(self.x), int(self.y))

    def ve(self, screen, cam_x, cam_y):

        screen.blit(self.image, (int(self.x - cam_x), int(self.y - cam_y)))