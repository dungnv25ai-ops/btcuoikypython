# the_gioi/vat_the.py — Các vật thể đặc biệt: Kiếm, Kẻ di chuyển
import pygame, math, random
from cai_dat import *

# ══════════════════════════════════════════════════════════
#  KIẾM — 1x2 dọc, màu vàng, nhấn F để nhặt
# ══════════════════════════════════════════════════════════
def _ve_kiem(ngang=False):
    if ngang:
        W, H = TILE_SIZE*2, TILE_SIZE
    else:
        W, H = TILE_SIZE, TILE_SIZE*2
    s = pygame.Surface((W, H), pygame.SRCALPHA)

    # Thân kiếm vàng
    pygame.draw.rect(s,(220,190,30),(2,2,W-4,H-4),border_radius=4)
    pygame.draw.rect(s,(255,230,80),(4,4,W-8,H-8),border_radius=3)

    if not ngang:
        # Lưỡi kiếm (phần trên)
        pygame.draw.rect(s,(240,240,180),(W//2-5,4,10,H*2//3))
        pygame.draw.polygon(s,(255,255,200),[(W//2-5,4),(W//2+5,4),(W//2,0)])
        # Chuôi (phần dưới)
        pygame.draw.rect(s,(180,140,20),(W//2-8,H*2//3,16,H//5),border_radius=2)
        # Guard ngang
        pygame.draw.rect(s,(200,160,30),(2,H*2//3-4,W-4,8),border_radius=3)
    else:
        # Lưỡi kiếm (phần phải)
        pygame.draw.rect(s,(240,240,180),(4,H//2-5,W*2//3,10))
        pygame.draw.polygon(s,(255,255,200),[(W-4,H//2-5),(W-4,H//2+5),(W,H//2)])
        # Chuôi (phần trái)
        pygame.draw.rect(s,(180,140,20),(W//5,H//2-8,W//5,16),border_radius=2)
        pygame.draw.rect(s,(200,160,30),(W*2//3-4,2,8,H-4),border_radius=3)

    pygame.draw.rect(s,(140,100,10),(0,0,W,H),2,border_radius=4)
    return s

class Kiem(pygame.sprite.Sprite):
    """Kiếm 1x2 — nhấn F khi gần để nhặt (biến mất)."""
    PHAM_VI = TILE_SIZE * 2   # khoảng cách nhặt

    def __init__(self, cot, hang, ngang=False):
        super().__init__()
        self.ngang   = ngang
        self.image   = _ve_kiem(ngang)
        self.rect    = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self.dem_nhip= 0
        self._alpha  = 255
        self._bien_mat = False
        self._alpha_giam = 0

    def gan_nguoi_choi(self, player_rect):
        return self.rect.inflate(self.PHAM_VI*2, self.PHAM_VI*2)\
                   .colliderect(player_rect)

    def bat_dau_bien_mat(self):
        self._bien_mat  = True
        self._alpha_giam = 18

    def update(self):
        self.dem_nhip += 1
        # Nhấp nháy nhẹ khi chờ
        if not self._bien_mat:
            a = int(220 + 35*math.sin(self.dem_nhip*0.08))
            self.image.set_alpha(a)
        else:
            self._alpha = max(0, self._alpha - self._alpha_giam)
            self.image.set_alpha(self._alpha)
            if self._alpha <= 0:
                self.kill()

    def ve_hint(self, screen, cam_x, cam_y, font):
        """Hiện chữ [F] phía trên kiếm."""
        t = font.render("[F] Nhặt kiếm", True, VANG)
        x = self.rect.centerx - cam_x - t.get_width()//2
        y = self.rect.top      - cam_y - 22
        bg = pygame.Surface((t.get_width()+8,t.get_height()+4),pygame.SRCALPHA)
        pygame.draw.rect(bg,(0,0,0,140),(0,0,*bg.get_size()),border_radius=4)
        screen.blit(bg,(x-4,y-2)); screen.blit(t,(x,y))


# ══════════════════════════════════════════════════════════
#  KẺ DI CHUYỂN — 1x1, đi qua nhân vật, chuột trái để diệt
# ══════════════════════════════════════════════════════════
def _ve_ke():
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    # Thân tím đỏ
    pygame.draw.rect(s,(160,50,180),(2,2,TILE_SIZE-4,TILE_SIZE-4),border_radius=6)
    pygame.draw.rect(s,(200,90,220),(4,4,TILE_SIZE-8,TILE_SIZE-8),border_radius=5)
    # Mắt
    pygame.draw.circle(s,(255,50,50),(14,16),5)
    pygame.draw.circle(s,(255,50,50),(TILE_SIZE-14,16),5)
    pygame.draw.circle(s,(255,200,200),(15,15),2)
    pygame.draw.circle(s,(255,200,200),(TILE_SIZE-13,15),2)
    # Miệng
    pygame.draw.arc(s,(255,80,80),(10,22,TILE_SIZE-20,12),math.pi,2*math.pi,2)
    pygame.draw.rect(s,(120,30,140),(0,0,TILE_SIZE,TILE_SIZE),2,border_radius=6)
    return s

class KeDiChuyen(pygame.sprite.Sprite):
    """Kẻ 1x1: đẩy + kill người chơi khi chạm. Chuột trái để diệt (cần kiếm)."""
    TOC_DO       = 1.5
    PHAM_VI_DAY  = TILE_SIZE * 1    # vùng đẩy
    PHAM_VI_DIET = TILE_SIZE * 2    # vùng diệt
    LUC_DAY      = 12               # lực đẩy ra
    I_FRAMES     = 40               # frame bất tử sau khi bị đẩy

    def __init__(self, cot, hang, bien_gioi_trai, bien_gioi_phai):
        super().__init__()
        self.image    = _ve_ke()
        self.rect     = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self._x       = float(self.rect.x)
        self.vel_x    = self.TOC_DO
        self.b_trai   = bien_gioi_trai * TILE_SIZE
        self.b_phai   = bien_gioi_phai * TILE_SIZE
        self.dem      = 0
        self._bien_mat= False
        self._alpha   = 255

    def gan_nguoi_choi(self, player_rect):
        return self.rect.inflate(self.PHAM_VI_DIET*2, self.PHAM_VI_DIET*2)\
                   .colliderect(player_rect)

    def kiem_tra_tan_cong(self, player_rect, i_frames):
        if self._bien_mat or i_frames > 0:
            return False, 0, 0
        if self.rect.colliderect(player_rect):
            dx = player_rect.centerx - self.rect.centerx
            dy = player_rect.centery - self.rect.centery
            dist = max(1, (dx**2+dy**2)**0.5)
            day_x = int(dx/dist * self.LUC_DAY)
            day_y = int(dy/dist * self.LUC_DAY - 4)
            return True, day_x, day_y
        return False, 0, 0

    def bat_dau_bien_mat(self):
        self._bien_mat = True

    # ---- CHÚ Ý: Thêm tham số ds_nen_tang vào hàm update ----
    def update(self, ds_nen_tang):
        self.dem += 1
        
        # Xử lý hiệu ứng biến mất khi bị giết
        if self._bien_mat:
            self._alpha = max(0, self._alpha - 20)
            self.image.set_alpha(self._alpha)
            if self._alpha <= 0: self.kill()
            return
            
        # 1. Di chuyển
        self._x += self.vel_x
        self.rect.x = int(self._x)

        # 2. Kiểm tra ĐỤNG TƯỜNG (cục gạch)
        dung_tuong = False
        for n in ds_nen_tang:
            if self.rect.colliderect(n.rect):
                dung_tuong = True
                if self.vel_x > 0:
                    self.rect.right = n.rect.left
                elif self.vel_x < 0:
                    self.rect.left = n.rect.right
                self._x = float(self.rect.x) # Ép lại tọa độ float
                break

        # 3. Kiểm tra VỰC THẲM (Cảm biến dưới mũi chân)
        co_dat_do = False
        if self.vel_x > 0:
            rect_cam_bien = pygame.Rect(self.rect.right + 2, self.rect.bottom + 2, 2, 2)
        else:
            rect_cam_bien = pygame.Rect(self.rect.left - 4, self.rect.bottom + 2, 2, 2)

        for n in ds_nen_tang:
            if rect_cam_bien.colliderect(n.rect):
                co_dat_do = True
                break

        # 4. XỬ LÝ QUAY ĐẦU (Nếu đụng tường, đụng vực, hoặc vượt quá biên cũ)
        if dung_tuong or not co_dat_do or self._x <= self.b_trai or self._x >= self.b_phai - self.rect.width:
            self.vel_x *= -1 # Đảo hướng
            
            # Khóa chặt trong biên b_trai/b_phai cũ đề phòng bị kẹt
            if self._x <= self.b_trai:
                self._x = float(self.b_trai)
                self.vel_x = abs(self.TOC_DO)
            elif self._x >= self.b_phai - self.rect.width:
                self._x = float(self.b_phai - self.rect.width)
                self.vel_x = -abs(self.TOC_DO)
                
            self.rect.x = int(self._x)

        # 5. Hiệu ứng nhấp nháy sáng (Code gốc của bạn)
        a = int(200+55*math.sin(self.dem*0.1))
        self.image.set_alpha(a)


# ══════════════════════════════════════════════════════════
#  SÁCH 1x1 — nhấn F để nhặt, mở khóa kỹ năng lướt
# ══════════════════════════════════════════════════════════
def _ve_sach():
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    # Bìa sách xanh
    pygame.draw.rect(s,(30,100,200),(2,2,TILE_SIZE-4,TILE_SIZE-4),border_radius=5)
    pygame.draw.rect(s,(60,140,240),(4,4,TILE_SIZE-8,TILE_SIZE-8),border_radius=4)
    # Trang giấy
    pygame.draw.rect(s,(240,235,200),(8,6,TILE_SIZE-16,TILE_SIZE-10),border_radius=3)
    # Chữ trên trang (3 dòng giả)
    for i in range(3):
        y = 12 + i*8
        pygame.draw.rect(s,(150,140,100),(10,y,TILE_SIZE-22,3))
    # Gáy sách
    pygame.draw.rect(s,(20,70,160),(2,2,5,TILE_SIZE-4),border_radius=3)
    # Biểu tượng chớp (kỹ năng)
    pts = [(TILE_SIZE-14,8),(TILE_SIZE-8,20),(TILE_SIZE-13,20),(TILE_SIZE-7,TILE_SIZE-8)]
    pygame.draw.polygon(s,(255,230,50),pts)
    pygame.draw.polygon(s,(200,170,20),pts,1)
    pygame.draw.rect(s,(15,60,140),(0,0,TILE_SIZE,TILE_SIZE),2,border_radius=5)
    return s

class Sach1x1(pygame.sprite.Sprite):
    """Sách 1x1 — nhấn F khi gần → mở khóa dash."""
    PHAM_VI = TILE_SIZE * 2

    def __init__(self, cot, hang):
        super().__init__()
        self.image   = _ve_sach()
        self.rect    = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self.dem     = 0
        self._bien_mat  = False
        self._alpha     = 255

    def gan_nguoi_choi(self, player_rect):
        return self.rect.inflate(self.PHAM_VI*2, self.PHAM_VI*2).colliderect(player_rect)

    def bat_dau_bien_mat(self):
        self._bien_mat = True

    def update(self):
        self.dem += 1
        if not self._bien_mat:
            a = int(210 + 45*math.sin(self.dem*0.07))
            self.image.set_alpha(a)
        else:
            self._alpha = max(0, self._alpha - 15)
            self.image.set_alpha(self._alpha)
            if self._alpha <= 0: self.kill()

    def ve_hint(self, screen, cam_x, cam_y, font):
        t = font.render("[F] Nhat sach ky nang", True, (100,200,255))
        x = self.rect.centerx - cam_x - t.get_width()//2
        y = self.rect.top - cam_y - 22
        bg = pygame.Surface((t.get_width()+8,t.get_height()+4),pygame.SRCALPHA)
        pygame.draw.rect(bg,(0,0,0,140),(0,0,*bg.get_size()),border_radius=4)
        screen.blit(bg,(x-4,y-2)); screen.blit(t,(x,y))


# ══════════════════════════════════════════════════════════
#  KHỐI DỊCH CHUYỂN 2x2 — chạm vào → teleport tới khu 3
# ══════════════════════════════════════════════════════════
def _ve_khoi_dc():
    W = TILE_SIZE*2
    s = pygame.Surface((W, W), pygame.SRCALPHA)
    # Nền tím huyền bí
    pygame.draw.rect(s,(80,20,160),(0,0,W,W),border_radius=8)
    pygame.draw.rect(s,(120,50,210),(3,3,W-6,W-6),border_radius=6)
    # Vòng xoáy đơn giản
    cx,cy = W//2,W//2
    for r,a in [(28,200),(20,160),(12,120)]:
        pygame.draw.circle(s,(160,80,255,a),(cx,cy),r,3)
    # Mũi tên dịch chuyển
    pygame.draw.polygon(s,(255,255,255),
        [(cx-14,cy),(cx,cy-16),(cx+14,cy),(cx+6,cy),(cx+6,cy+16),(cx-6,cy+16),(cx-6,cy)])
    # Viền sáng
    pygame.draw.rect(s,(180,100,255),(0,0,W,W),3,border_radius=8)
    return s

class KhoiDichChuyen(pygame.sprite.Sprite):
    """Khối 2x2 — khi nhân vật chạm → teleport."""
    def __init__(self, cot, hang):
        super().__init__()
        self.image   = _ve_khoi_dc()
        self.rect    = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self.dem     = 0
        self.da_dich = False

    def update(self):
        self.dem += 1
        a = int(180 + 75*math.sin(self.dem*0.06))
        self.image.set_alpha(a)


# ══════════════════════════════════════════════════════════
#  SÁCH 1x1 — nhấn F để mở khóa kỹ năng dash
# ══════════════════════════════════════════════════════════
def _ve_sach():
    s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    # Bìa sách xanh
    pygame.draw.rect(s,(30,100,200),(2,2,TILE_SIZE-4,TILE_SIZE-4),border_radius=5)
    pygame.draw.rect(s,(60,140,240),(4,4,TILE_SIZE-8,TILE_SIZE-8),border_radius=4)
    # Trang sách
    pygame.draw.rect(s,(240,235,210),(8,8,TILE_SIZE-16,TILE_SIZE-16),border_radius=2)
    # Chữ trên trang
    for y in [16,22,28,34]:
        pygame.draw.line(s,(150,140,120),(10,y),(TILE_SIZE-10,y),1)
    # Icon tia sét (dash)
    pts=[(TILE_SIZE//2+2,10),(TILE_SIZE//2-4,22),(TILE_SIZE//2+2,22),(TILE_SIZE//2-4,36)]
    pygame.draw.lines(s,(255,200,0),False,pts,3)
    # Viền
    pygame.draw.rect(s,(20,60,150),(2,2,TILE_SIZE-4,TILE_SIZE-4),2,border_radius=5)
    return s

class Sach1x1(pygame.sprite.Sprite):
    """Sách 1x1 — nhặt bằng F, mở khóa dash."""
    PHAM_VI = TILE_SIZE * 2

    def __init__(self, cot, hang):
        super().__init__()
        self.image    = _ve_sach()
        self.rect     = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self.dem      = 0
        self._bien_mat= False
        self._alpha   = 255

    def gan_nguoi_choi(self, player_rect):
        return self.rect.inflate(self.PHAM_VI*2, self.PHAM_VI*2).colliderect(player_rect)

    def bat_dau_bien_mat(self):
        self._bien_mat = True

    def update(self):
        self.dem += 1
        if not self._bien_mat:
            a = int(210 + 45*math.sin(self.dem*0.09))
            self.image.set_alpha(a)
        else:
            self._alpha = max(0, self._alpha - 18)
            self.image.set_alpha(self._alpha)
            if self._alpha <= 0: self.kill()

    def ve_hint(self, screen, cam_x, cam_y, font):
        t = font.render("[F] Nhan sach: mo khoa Dash", True, (100,200,255))
        x = self.rect.centerx - cam_x - t.get_width()//2
        y = self.rect.top - cam_y - 22
        bg = pygame.Surface((t.get_width()+8,t.get_height()+4),pygame.SRCALPHA)
        pygame.draw.rect(bg,(0,0,0,140),(0,0,*bg.get_size()),border_radius=4)
        screen.blit(bg,(x-4,y-2)); screen.blit(t,(x,y))


# ══════════════════════════════════════════════════════════
#  KHỐI DỊCH CHUYỂN 2x2 — chạm vào → teleport
# ══════════════════════════════════════════════════════════
def _ve_khoi_dc():
    W, H = TILE_SIZE*2, TILE_SIZE*2
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    # Nền tím
    pygame.draw.rect(s,(100,30,180),(0,0,W,H),border_radius=8)
    pygame.draw.rect(s,(140,70,220),(2,2,W-4,H-4),border_radius=7)
    # Vòng xoáy/portal
    cx,cy = W//2, H//2
    for r,a,c in [(36,255,(200,150,255)),(28,200,(180,120,255)),(20,160,(160,100,240))]:
        surf_c = pygame.Surface((r*2,r*2),pygame.SRCALPHA)
        pygame.draw.circle(surf_c,c+(a,),(r,r),r)
        s.blit(surf_c,(cx-r,cy-r))
    pygame.draw.circle(s,(255,255,255,230),(cx,cy),8)
    # Tia sáng
    for ang in range(0,360,45):
        rad = math.radians(ang)
        x1=int(cx+12*math.cos(rad)); y1=int(cy+12*math.sin(rad))
        x2=int(cx+22*math.cos(rad)); y2=int(cy+22*math.sin(rad))
        pygame.draw.line(s,(220,180,255,180),(x1,y1),(x2,y2),2)
    # Viền
    pygame.draw.rect(s,(180,100,255),(0,0,W,H),3,border_radius=8)
    return s

class KhoiDichChuyen(pygame.sprite.Sprite):
    """Khối teleport. Mặc định 2x2."""
    def __init__(self, cot, hang, dich_den_cot=42, dich_den_hang=5, rong=2, cao=2):
        super().__init__()
        W = TILE_SIZE*rong; H = TILE_SIZE*cao
        s = pygame.Surface((W,H),pygame.SRCALPHA)
        # Vẽ portal
        import math as _m
        pygame.draw.rect(s,(100,30,180),(0,0,W,H),border_radius=8)
        pygame.draw.rect(s,(140,70,220),(2,2,W-4,H-4),border_radius=7)
        cx,cy=W//2,H//2
        for r,a,c in [(min(W,H)//2-4,200,(200,150,255)),(min(W,H)//2-10,180,(180,120,255))]:
            gs=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
            pygame.draw.circle(gs,c+(a,),(r,r),r)
            s.blit(gs,(cx-r,cy-r))
        pygame.draw.circle(s,(255,255,255,220),(cx,cy),6)
        for ang in range(0,360,60):
            rd=_m.radians(ang)
            x1=int(cx+10*_m.cos(rd)); y1=int(cy+10*_m.sin(rd))
            x2=int(cx+18*_m.cos(rd)); y2=int(cy+18*_m.sin(rd))
            pygame.draw.line(s,(220,180,255,160),(x1,y1),(x2,y2),2)
        pygame.draw.rect(s,(180,100,255),(0,0,W,H),3,border_radius=8)
        self._surf_orig    = s
        self.image         = self._surf_orig.copy()
        self.rect          = self.image.get_rect(topleft=(cot*TILE_SIZE, hang*TILE_SIZE))
        self.dem           = 0
        self.dich_cot      = dich_den_cot
        self.dich_hang     = dich_den_hang
        # Vị trí cổng (để biết chiều teleport)
        self._cot_cong     = cot
        self._hang_cong    = hang
        # Hội thoại cổng
        self._trong_vung   = False   # player đang trong vùng
        self._hoi_thoai_hien = False  # đang hiện hội thoại
        self._cho_tra_loi  = False   # đang chờ Y/N
        self.font          = None

    def _init_font(self):
        if not self.font:
            self.font = pygame.font.SysFont(FONT_CHINH, 16)

    def update(self):
        self.dem += 1
        a = int(180+75*abs(math.sin(self.dem*0.06)))
        self.image = self._surf_orig.copy()
        self.image.set_alpha(a)

    def xu_ly_vung(self, player_rect):
        """Gọi mỗi frame. Trả về True nếu cần hiện hội thoại lần đầu."""
        dang_trong = self.rect.inflate(TILE_SIZE,TILE_SIZE).colliderect(player_rect)
        if dang_trong and not self._trong_vung:
            # Vừa bước vào
            self._hoi_thoai_hien = True
            self._cho_tra_loi    = True
        if not dang_trong and self._trong_vung:
            # Bước ra → reset để hiện lại lần sau
            self._hoi_thoai_hien = False
            self._cho_tra_loi    = False
        self._trong_vung = dang_trong
        return self._hoi_thoai_hien

    def tra_loi_co(self, player_rect=None):
        """Người chơi chọn Có → trả về tọa độ đích.
        Nếu player ở bên phải cổng → teleport về cot_cong-3 (chiều ngược).
        Nếu player ở bên trái cổng → teleport đến dich_cot (chiều tiến).
        """
        self._hoi_thoai_hien = False
        self._cho_tra_loi    = False
        if player_rect is not None:
            # Player bên phải cổng → đi ngược về
            if player_rect.centerx > (self._cot_cong + 2) * TILE_SIZE:
                return ((self._cot_cong - 3) * TILE_SIZE, self.dich_hang * TILE_SIZE)
        return (self.dich_cot * TILE_SIZE, self.dich_hang * TILE_SIZE)

    def tra_loi_khong(self):
        """Người chơi chọn Không → đóng hội thoại, KHÔNG teleport."""
        self._hoi_thoai_hien = False
        self._cho_tra_loi    = False

    def ve_hoi_thoai(self, screen, cam_x, cam_y, mw, mh):
        if not self._hoi_thoai_hien: return
        self._init_font()
        font_to = pygame.font.SysFont(FONT_CHINH, 18, bold=True)
        cx = self.rect.centerx - cam_x
        cy = self.rect.top     - cam_y - 10

        BW, BH = 300, 100
        bx = max(8, min(cx-BW//2, mw-BW-8))
        by = max(8, cy-BH-10)

        bong = pygame.Surface((BW,BH),pygame.SRCALPHA)
        pygame.draw.rect(bong,(20,10,40,230),(0,0,BW,BH),border_radius=10)
        pygame.draw.rect(bong,(180,100,255,255),(0,0,BW,BH),2,border_radius=10)
        screen.blit(bong,(bx,by))

        t1 = font_to.render("Ban co muon di vao khong?",True,(220,180,255))
        screen.blit(t1,t1.get_rect(center=(bx+BW//2,by+28)))

        # Nút Y / N
        for i,(lbl,mau) in enumerate([("Y  Co",(80,200,80)),("N  Khong",(200,80,80))]):
            rr = pygame.Rect(bx+30+i*150, by+58, 110, 30)
            mx,my2=pygame.mouse.get_pos()
            hv=rr.collidepoint(mx,my2)
            pygame.draw.rect(screen,tuple(min(c+40,255) for c in mau) if hv else mau,rr,border_radius=6)
            t2=self.font.render(lbl,True,TRANG)
            screen.blit(t2,t2.get_rect(center=rr.center))

        # Lưu rect nút để bắt click
        self._rect_co   = pygame.Rect(bx+30,  by+58, 110, 30)
        self._rect_khong= pygame.Rect(bx+180, by+58, 110, 30)

    def xu_ly_click_hoi_thoai(self, ev_pos):
        """Trả về 'co', 'khong', hoặc None."""
        if not self._cho_tra_loi: return None
        if hasattr(self,'_rect_co')   and self._rect_co.collidepoint(ev_pos):   return 'co'
        if hasattr(self,'_rect_khong') and self._rect_khong.collidepoint(ev_pos): return 'khong'
        return None


# ══════════════════════════════════════════════════════════
#  KHỐI RƠI — 1x2 ngang hoặc dọc, rơi từ trên, chạm = chết
# ══════════════════════════════════════════════════════════
def _ve_khoi_roi(ngang=False):
    if ngang:
        W, H = TILE_SIZE*2, TILE_SIZE
    else:
        W, H = TILE_SIZE, TILE_SIZE*2
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    # Nền đỏ nguy hiểm
    pygame.draw.rect(s,(180,30,30),(0,0,W,H),border_radius=4)
    pygame.draw.rect(s,(220,60,60),(2,2,W-4,H-4),border_radius=3)
    # Vân xéo cảnh báo
    import math as _m
    for i in range(-max(W,H), max(W,H), 12):
        x1=max(0,i); y1=max(0,-i)
        x2=min(W,i+H); y2=min(H,-i+W)
        if x1<W and y1<H and x2>0 and y2>0:
            pygame.draw.line(s,(240,90,40,180),(x1,y1),(x2,y2),3)
    # Mũi tên chỉ xuống
    cx,cy=W//2,H//2
    pygame.draw.polygon(s,(255,220,0),[
        (cx-6,cy-8),(cx+6,cy-8),(cx+6,cy+2),(cx+12,cy+2),(cx,cy+12),(cx-12,cy+2),(cx-6,cy+2)
    ])
    pygame.draw.rect(s,(140,20,20),(0,0,W,H),2,border_radius=4)
    return s

class KhoiRoi(pygame.sprite.Sprite):
    """Khối 1x2 rơi từ trên, chạm nhân vật = chết."""
    TRONG_LUC = 0.5
    TOC_DO_MAX = 12

    def __init__(self, cot, hang_bat_dau, ngang=False, tri_hoan=0):
        """
        cot, hang_bat_dau: vị trí xuất phát (tile)
        ngang: True=1x2 nằm ngang, False=1x2 đứng dọc
        tri_hoan: số frame chờ trước khi bắt đầu rơi
        """
        super().__init__()
        self.ngang       = ngang
        self.image       = _ve_khoi_roi(ngang)
        self.rect        = self.image.get_rect(
            topleft=(cot*TILE_SIZE, hang_bat_dau*TILE_SIZE))
        self._y_float    = float(self.rect.y)
        self._vel_y      = 0.0
        self._tri_hoan   = tri_hoan    # frame delay trước khi rơi
        self._da_roi     = False
        self._dem        = 0
        self._alpha      = 255
        self._bien_mat   = False
        self._bien_mat_t = 0

    def update(self, ds_nen):
        if self._bien_mat:
            # Biến mất sau khi giết player
            self._bien_mat_t += 1
            if self._bien_mat_t > 30:
                self.image.set_alpha(max(0, 255-self._bien_mat_t*8))
            if self._bien_mat_t > 62:
                self.kill()
            return

        self._dem += 1

        # Chờ delay rồi mới rơi
        if self._dem <= self._tri_hoan:
            # Nhấp nháy nhẹ báo hiệu sắp rơi
            if self._tri_hoan - self._dem < 60:
                a = int(140 + 115*abs(math.sin(self._dem*0.3)))
                self.image.set_alpha(a)
            return

        self._da_roi = True
        # Vật lý rơi
        self._vel_y = min(self._vel_y + self.TRONG_LUC, self.TOC_DO_MAX)
        self._y_float += self._vel_y
        self.rect.y = int(self._y_float)

        # Va chạm với nền (dừng lại khi chạm đất)
        for n in ds_nen:
            if self.rect.colliderect(n.rect) and self._vel_y > 0:
                self.rect.bottom = n.rect.top
                self._y_float    = float(self.rect.y)
                self._vel_y      = 0
                break

    def kiem_tra_cham_nguoi(self, player_rect):
        """Trả về True nếu đang rơi và chạm nhân vật."""
        if not self._da_roi or self._bien_mat: return False
        return self.rect.colliderect(player_rect)

    def bat_dau_bien_mat(self):
        self._bien_mat   = True
        self._bien_mat_t = 0

    def ve_canh_bao(self, screen, cam_x, cam_y, font):
        """Vẽ mũi tên cảnh báo phía trên nếu chưa lọt vào màn hình."""
        if self._bien_mat or not self._da_roi: return
        sx = self.rect.centerx - cam_x
        sy = self.rect.top     - cam_y
        if sy < 0:   # khối đang ở trên màn hình
            w = screen.get_width()
            if 0 <= sx <= w:
                # Vẽ mũi tên cảnh báo ở mép trên
                pygame.draw.polygon(screen,(255,60,60),[
                    (sx-10,5),(sx+10,5),(sx,22)
                ])
                pygame.draw.polygon(screen,(255,200,0),[
                    (sx-10,5),(sx+10,5),(sx,22)
                ],2)


# ══════════════════════════════════════════════════════════
#  QUẢ CẦU NÉM — boss 5,10 tụ lực rồi bắn thẳng
# ══════════════════════════════════════════════════════════
def _ve_qua_cau(r=14):
    S=r*2+4
    s=pygame.Surface((S,S),pygame.SRCALPHA)
    pygame.draw.circle(s,(220,80,80,200),(S//2,S//2),r)
    pygame.draw.circle(s,(255,140,100,220),(S//2-4,S//2-4),r//2)
    pygame.draw.circle(s,(255,60,60,255),(S//2,S//2),r,2)
    return s

class QuaCau(pygame.sprite.Sprite):
    """Quả cầu bắn thẳng từ boss đến player."""
    TOC_DO = 5

    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = _ve_qua_cau()
        self.rect  = self.image.get_rect(center=(x,y))
        self._x    = float(x); self._y = float(y)
        dx = target_x - x; dy = target_y - y
        dist = max(1,(dx**2+dy**2)**0.5)
        self._vx = dx/dist*self.TOC_DO
        self._vy = dy/dist*self.TOC_DO
        self._dem = 0

    def update(self):
        self._dem += 1
        self._x += self._vx; self._y += self._vy
        self.rect.center = (int(self._x), int(self._y))
        # Tự xóa sau 5s
        if self._dem > 300: self.kill()

    def cham_nguoi(self, player_rect):
        return self.rect.colliderect(player_rect)
