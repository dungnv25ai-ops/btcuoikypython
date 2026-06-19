                                                    
import pygame
import os
from cai_dat import *

T = TILE_SIZE

_THU_MUC_GD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CACHE_TROI_CHAN = []

def _load_troi_chan():
    global _CACHE_TROI_CHAN
    if _CACHE_TROI_CHAN:
        return _CACHE_TROI_CHAN
    thu_muc = os.path.join(_THU_MUC_GD, "tai_nguyen", "skill", "troi_chan")
    if not os.path.isdir(thu_muc):
        return _CACHE_TROI_CHAN
    for i in range(1, 61):
        path = os.path.join(thu_muc, f"{i}.png")
        if not os.path.isfile(path):
            break
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (T, T))
            _CACHE_TROI_CHAN.append(img)
        except Exception:
            pass
    return _CACHE_TROI_CHAN

def _ve_fallback():
    s = pygame.Surface((T, T), pygame.SRCALPHA)
    pygame.draw.rect(s, (180, 80, 20, 200), (4, 4, T-8, T-8), border_radius=6)
    pygame.draw.rect(s, (240, 140, 40, 255), (4, 4, T-8, T-8), 2, border_radius=6)
                          
    for y in range(6, T-6, 8):
        pygame.draw.ellipse(s, (220, 160, 60, 220), (T//2-8, y, 16, 6))
    return s

class HieuUngTroiChan:

    TONG_GIAY    = 5.0
    XUAT_HIEN    = 2.0                 
    DUY_TRI      = 1.0                
    BIEN_MAT     = 2.0                 
    KHOA_BAT_DAU = 1.0                      
    KHOA_KET_THUC= 4.0                       

    SPD = 2

    def __init__(self):
        self._active  = False
        self._dem     = 0                       
        self._frames  = []
        self.image    = None
        self._fallback= None

    @property
    def dang_hoat_dong(self):
        return self._active

    @property
    def dang_khoa(self):

        if not self._active:
            return False
        giay = self._dem / FPS
        return self.KHOA_BAT_DAU <= giay < self.KHOA_KET_THUC

    def bat_dau(self):
                                       
        if self._active:
            return

        self._active = True
        self._dem    = 0
        self._frames = _load_troi_chan()
        if not self._fallback:
            self._fallback = _ve_fallback()

    def _lay_anh(self):

        frames = self._frames
        n = len(frames) if frames else 0
        giay  = self._dem / FPS

        if n == 0:
                                                            
            if self.dang_khoa:
                s = self._fallback.copy()
                s.set_alpha(int(200 * min(1.0, (giay - self.KHOA_BAT_DAU) /
                                           self.XUAT_HIEN)))
                return s
            return None

        if giay < self.XUAT_HIEN:
                                      
            tl  = giay / self.XUAT_HIEN
            idx = min(int(tl * n), n - 1)
        elif giay < self.XUAT_HIEN + self.DUY_TRI:
                                  
            idx = n - 1
        else:
                                      
            tl  = (giay - self.XUAT_HIEN - self.DUY_TRI) / self.BIEN_MAT
                                                                                      
            idx = min(n - 1, max(0, int((1.0 - tl) * n)))

        return frames[idx]

    def update(self, nhan_vat):
        if not self._active:
            return

        self._dem += 1

        if self._dem >= int(self.TONG_GIAY * FPS):
            self._active = False
            self._mo_khoa(nhan_vat)
            self.image = None
            return

        self.image = self._lay_anh()

        if self.dang_khoa:
            self._khoa_nhan_vat(nhan_vat)
        else:
            self._mo_khoa(nhan_vat)

    def _khoa_nhan_vat(self, nv):

        nv.vel_x = 0
                                            
        nv.vel_y = 0
                                
        nv._dash_frames = 0
                 
        nv._bay_active  = False
                        
        nv._danh_signal = False
        nv._nem_signal  = False
                                                 
        nv._khoa_hieu_ung = True

    def _mo_khoa(self, nv):
        nv._khoa_hieu_ung = False

    def ve(self, screen, cam_x, cam_y, nhan_vat):

        if not self._active or self.image is None:
            return
                                   
        x = nhan_vat.rect.centerx - T//2 - cam_x
        y = nhan_vat.rect.bottom  - T    - cam_y
        screen.blit(self.image, (x, y))

_CACHE_DONG_BANG = []                            

def _load_dong_bang():
    global _CACHE_DONG_BANG
    if _CACHE_DONG_BANG:
        return _CACHE_DONG_BANG
    thu_muc = os.path.join(_THU_MUC_GD, "tai_nguyen", "skill", "dong_bang")
    if not os.path.isdir(thu_muc):
        return _CACHE_DONG_BANG
    for i in range(1, 5):
        path = os.path.join(thu_muc, f"{i}.png")
        if not os.path.isfile(path):
            break
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (T * 2, T * 2))
            _CACHE_DONG_BANG.append(img)
        except Exception:
            pass
    return _CACHE_DONG_BANG

def _ve_fallback_dong_bang(cap):

    W = T * 2
    s = pygame.Surface((W, W), pygame.SRCALPHA)
    alpha = 80 + cap * 45                                      
    mau   = (60, 180, 240, alpha)
    vien  = (140, 220, 255, 255)
    pygame.draw.rect(s, mau,  (2, 2, W-4, W-4), border_radius=10)
    pygame.draw.rect(s, vien, (2, 2, W-4, W-4), 2, border_radius=10)
                               
    cx, cy = W // 2, W // 2
    for ang in range(0, 360, 60):
        import math
        rad = math.radians(ang)
        ex  = cx + int((W // 2 - 8) * math.cos(rad))
        ey  = cy + int((W // 2 - 8) * math.sin(rad))
        pygame.draw.line(s, vien, (cx, cy), (ex, ey), 2)
    return s

class HieuUngDongBang:

    SO_LAN_PHA = 4                            

    def __init__(self):
        self._active  = False
        self._cap     = 0                                     
        self._frames  = []
        self._fallbacks = []
        self.image    = None

    @property
    def dang_hoat_dong(self):
        return self._active

    def bat_dau(self):

        if self._active:
            return
        self._active = True
        self._cap    = 0
        self._frames = _load_dong_bang()
        if not self._fallbacks:
            self._fallbacks = [_ve_fallback_dong_bang(c) for c in range(4)]
        self.image = self._lay_anh()

    def nhan_danh(self, nhan_vat=None):

        if not self._active:
            return
        self._cap += 1
        if self._cap >= self.SO_LAN_PHA:
            self._active = False
            self.image   = None
            if nhan_vat is not None:
                nhan_vat._khoa_dong_bang = False
        else:
            self.image = self._lay_anh()

    def _lay_anh(self):

        idx = min(self._cap, self.SO_LAN_PHA - 1)
        if self._frames and idx < len(self._frames):
            return self._frames[idx]
                  
        if self._fallbacks and idx < len(self._fallbacks):
            return self._fallbacks[idx]
        return None

    def update(self, nhan_vat):
        if not self._active:
            return

        nhan_vat.vel_x        = 0
        nhan_vat.vel_y        = 0
        nhan_vat._dash_frames = 0
        nhan_vat._bay_active  = False
        nhan_vat._nem_signal  = False
                                                           
        nhan_vat._khoa_dong_bang = True

    def ket_thuc(self, nhan_vat):

        nhan_vat._khoa_dong_bang = False

    def ve(self, screen, cam_x, cam_y, nhan_vat):

        if not self._active or self.image is None:
            return
        W = T * 2
        x = nhan_vat.rect.centerx - W // 2 - cam_x
        y = nhan_vat.rect.centery - W // 2 - cam_y
        screen.blit(self.image, (x, y))

_CACHE_BAT_TU = None                   

def _load_bat_tu():
    global _CACHE_BAT_TU
    if _CACHE_BAT_TU is not None:
        return _CACHE_BAT_TU
    path = os.path.join(_THU_MUC_GD, "tai_nguyen", "skill", "battu.png")
    if os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
                                                
            img = pygame.transform.scale(img, (T*2, T * 2))
            _CACHE_BAT_TU = img
        except Exception:
            pass
    if _CACHE_BAT_TU is None:
                                       
        s = pygame.Surface((T, T * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(s, (255, 220, 50, 160), (2, 2, T-4, T*2-4))
        pygame.draw.ellipse(s, (255, 255, 150, 220), (2, 2, T-4, T*2-4), 3)
        _CACHE_BAT_TU = s
    return _CACHE_BAT_TU

class HieuUngBatTu:

    TONG_GIAY    = 3                                     
    TONG_FRAME   = TONG_GIAY * FPS
    NHAP_NHAY_TU = 2 * FPS                                                   
    NHAP_NHAY_CK = 6                                             

    def __init__(self):
        self._active = False
        self._dem    = 0
        self._anh    = None
        self.image   = None                                      

    @property
    def dang_hoat_dong(self):
        return self._active

    def bat_dau(self):

        self._active = True
        self._dem    = 0
        self._anh    = _load_bat_tu()
        self.image   = self._anh

    def update(self, nhan_vat):
        if not self._active:
            return

        self._dem += 1

        if self._dem >= self.TONG_FRAME:
            self._active = False
            self.image   = None
            return

        con_lai = self.TONG_FRAME - self._dem
        if con_lai <= FPS:
                                                     
            hien = (self._dem // self.NHAP_NHAY_CK) % 2 == 0
            self.image = self._anh if hien else None
        else:
            self.image = self._anh

    def ve(self, screen, cam_x, cam_y, nhan_vat):

        if not self._active or self.image is None:
            return
        x = nhan_vat.rect.x - cam_x
        y = nhan_vat.rect.y - cam_y
        screen.blit(self.image, (x, y))

_CACHE_TAN_CONG = None                                    
_CACHE_KIEM_CAM = None                                     

def _load_tan_cong():
    global _CACHE_TAN_CONG
    if _CACHE_TAN_CONG is not None:
        return _CACHE_TAN_CONG
    path = os.path.join(_THU_MUC_GD, "tai_nguyen", "hinh_anh", "nhan_vat", "tancong.png")
    if os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (T*2, T*2))
            _CACHE_TAN_CONG = img
            return img
        except Exception:
            pass
    s = pygame.Surface((T*2, T*2), pygame.SRCALPHA)
    pygame.draw.line(s, (255,255,255,220), (T*2-6, 6), (6, T*2-6), 8)
    _CACHE_TAN_CONG = s
    return s

def _load_kiem_cam():

    global _CACHE_KIEM_CAM
    if _CACHE_KIEM_CAM is not None:
        return _CACHE_KIEM_CAM
    path = os.path.join(_THU_MUC_GD, "tai_nguyen", "hinh_anh", "nhan_vat", "kiem.png")
    if os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
                                                                         
            ow, oh = img.get_size()
                                                             
            img = pygame.transform.scale(img, (T // 2, T * 2))
            _CACHE_KIEM_CAM = img
            return img
        except Exception:
            pass
              
    s = pygame.Surface((T//2, T*2), pygame.SRCALPHA)
    pygame.draw.rect(s, (200, 200, 220), (s.get_width()//2-3, 0, 6, T*2), border_radius=2)
    _CACHE_KIEM_CAM = s
    return s

class HieuUngTanCong:

    FRAME_GIAI_DOAN_1 = 6                              
    FRAME_GIAI_DOAN_2 = 24                         
    TONG_FRAME = FRAME_GIAI_DOAN_1 + FRAME_GIAI_DOAN_2                   

    def __init__(self):
        self._active    = False
        self._dem       = 0
        self._huong     = 1
        self._anh       = None
        self._anh_flip  = None
        self._kiem      = None
        self._kiem_flip = None
        self.image      = None                                 
        self.rect       = None
                                   
        self.dang_gd1   = False                                          
                                                        
        self.dang_danh  = False

    @property
    def can_khoa_di_chuyen(self):

        return self._active and self._dem < self.FRAME_GIAI_DOAN_1

    def kich_hoat(self, player_rect, huong):
        if self._anh is None:
            self._anh      = _load_tan_cong()
            self._anh_flip = pygame.transform.flip(self._anh, True, False)
        if self._kiem is None:
            k = _load_kiem_cam()
            self._kiem      = k
            self._kiem_flip = pygame.transform.flip(k, True, False)

        self._active   = True
        self._dem      = 0
        self._huong    = huong
        self.dang_danh = True
        self.dang_gd1  = True
        self.image     = None
        self.rect      = None
        self._player_rect = player_rect.copy()

    def update(self, nhan_vat=None):
        if not self._active:
            self.dang_danh = False
            self.dang_gd1  = False
            return

        self._dem += 1

        if nhan_vat is not None:
            self._player_rect = nhan_vat.rect.copy()

        if self._dem <= self.FRAME_GIAI_DOAN_1:
            self.dang_gd1  = True
            self.image     = None
            self.rect      = None
                                                      
            if nhan_vat is not None:
                nhan_vat.vel_x        = 0
                nhan_vat._dash_frames = 0

        else:
            self.dang_gd1 = False
            anh = self._anh if self._huong == 1 else self._anh_flip
            self.image = anh
            pr = self._player_rect
            if self._huong == 1:
                self.rect = anh.get_rect(midleft=(pr.centerx - T, pr.centery))
            else:
                self.rect = anh.get_rect(midright=(pr.centerx + T, pr.centery))

        if self._dem >= self.TONG_FRAME:
            self._active   = False
            self.dang_danh = False
            self.dang_gd1  = False
            self.image     = None
            self.rect      = None

    def ve_giai_doan_1(self, screen, cam_x, cam_y):

        if not self.dang_gd1 or self._kiem is None:
            return
        pr = self._player_rect
        anh = self._kiem if self._huong == 1 else self._kiem_flip
                                                             
        if self._huong == 1:
            x = pr.right - T // 4 - cam_x
        else:
            x = pr.left - T // 4 - cam_x
        y = pr.centery - T - cam_y                                  
        screen.blit(anh, (x, y))

    def ve(self, screen, cam_x, cam_y):

        if not self._active or self.image is None or self.rect is None:
            return
        screen.blit(self.image, (self.rect.x - cam_x, self.rect.y - cam_y))

class HieuUngBay:

    def __init__(self):
        self._active = False
        self._dem    = 0
        self._tong   = 0

    @property
    def dang_hoat_dong(self):
        return self._active

    def bat_dau(self, thoi_gian=60):
        if self._active:
            self._tong += thoi_gian             
        else:
            self._active = True
            self._dem    = 0
            self._tong   = thoi_gian

    def update(self, nhan_vat):
        if not self._active:
            return
        nhan_vat.vel_y = 0                     
        self._dem += 1
        if self._dem >= self._tong:
            self._active = False
            self._dem    = 0
            self._tong   = 0

class HieuUngStchuan:

    def __init__(self):
        self._pending = False                               

    def bat_dau(self):
        self._pending = True

    def xu_ly(self, hud, nhan_vat, spawn_pos):

        if not self._pending:
            return False
        self._pending = False
        game_over = hud.mat_mang()
                                               
        nhan_vat.rect.topleft = spawn_pos
        nhan_vat.vel_x = 0
        nhan_vat.vel_y = 0
        return game_over

class QuanLyHieuUng:

    def __init__(self):
        self.troi_chan = HieuUngTroiChan()
        self.dong_bang = HieuUngDongBang()
        self.bat_tu    = HieuUngBatTu()
        self.tan_cong  = HieuUngTanCong()
        self.bay       = HieuUngBay()
        self.stchuan   = HieuUngStchuan()

    def kich_hoat(self, ten, **kwargs):
        if ten == 'troi_chan':
            self.troi_chan.bat_dau()
        elif ten == 'dong_bang':
            self.dong_bang.bat_dau()
        elif ten == 'bat_tu':
            self.bat_tu.bat_dau()
        elif ten == 'bay':
            self.bay.bat_dau(kwargs.get('thoi_gian', 120))
        elif ten == 'stchuan':
            self.stchuan.bat_dau()

    @property
    def dang_bi_troi(self):
        return self.troi_chan.dang_khoa

    @property
    def dang_bi_dong_bang(self):
        return self.dong_bang.dang_hoat_dong

    @property
    def dang_bat_tu(self):
        return self.bat_tu.dang_hoat_dong

    @property
    def dang_bay(self):
        return self.bay.dang_hoat_dong

    def update(self, nhan_vat):
        self.troi_chan.update(nhan_vat)
        if self.dong_bang.dang_hoat_dong:
            self.dong_bang.update(nhan_vat)
        else:
            if hasattr(nhan_vat, '_khoa_dong_bang') and nhan_vat._khoa_dong_bang:
                self.dong_bang.ket_thuc(nhan_vat)
        self.bat_tu.update(nhan_vat)
        self.tan_cong.update(nhan_vat)
                                                   
        self.bay.update(nhan_vat)

    def ve(self, screen, cam_x, cam_y, nhan_vat):
        self.troi_chan.ve(screen, cam_x, cam_y, nhan_vat)
        self.dong_bang.ve(screen, cam_x, cam_y, nhan_vat)
        self.bat_tu.ve(screen, cam_x, cam_y, nhan_vat)
        self.tan_cong.ve_giai_doan_1(screen, cam_x, cam_y)
        self.tan_cong.ve(screen, cam_x, cam_y)