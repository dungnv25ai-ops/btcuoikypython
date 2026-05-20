# man_hinh/man_choi.py
import pygame
from cai_dat import *
from the_gioi.nhan_vat  import NhanVat
from the_gioi.nen_tang  import NenTang, NenTangBoss, KhucGo, ODict
from the_gioi.tinh_linh import TinhLinh
from the_gioi.tinh_linh_dieu_khien import TinhLinhDieuKhien
from the_gioi.vat_the   import Kiem, KeDiChuyen, Sach1x1, KhoiDichChuyen, KhoiRoi, QuaCau, KhoiNuoc, KiemBay, KiemMua, KiemNem
from the_gioi.boss       import Boss5, Boss10
from tien_ich.camera      import Camera
from tien_ich.hud          import HUD
from tien_ich.man_ket_qua  import ManKetQua

T = TILE_SIZE

# ══════════════════════════════════════════════════════════
#  MAP 1
# ══════════════════════════════════════════════════════════
def _gen_map1():
    R,C=11,80
    m=[[' ']*C for _ in range(R)]
    def fill(r1,r2,c1,c2,ch='#'):
        for r in range(r1,r2):
            for c in range(c1,c2):
                if 0<=r<R and 0<=c<C: m[r][c]=ch
    fill(8,11,0,80)
    m[6][1]='P'
    fill(1,2,25,27); fill(3,4,31,33); fill(5,6,25,27)
    m[0][25]='$'; m[2][31]='$'; m[4][25]='$'
    m[7][30]='#'
    fill(4,8,51,60); fill(3,8,60,80)
    m[3][59]='*'; m[2][59]='*'; m[1][59]='*'; m[0][59]='*'
    return [''.join(r) for r in m]

def _gen_map2():
    R,C=11,80
    m=[[' ']*C for _ in range(R)]
    def fill(r1,r2,c1,c2,ch='#'):
        for r in range(r1,r2):
            for c in range(c1,c2):
                if 0<=r<R and 0<=c<C: m[r][c]=ch
    fill(8,11,0,21);fill(10,11,21,26)
    fill(8,11,26,80); m[7][26]='E'; fill(7,8,29,30);m[9][23]='$'
    m[6][1]='P'; m[6][10]='K'
    fill(2,3,25,28); fill(2,3,35,38);fill(2,3,45,48); fill(2,3,55,58);fill(2,3,65,68); fill(2,9,75,80)
    m[1][26]='E'; m[1][36]='E'
    m[1][79]='*';m[0][79]='*'
    m[0][26]='$'; m[0][56]='$'
    return [''.join(r) for r in m]

MAP_1 = _gen_map1()
MAP_2 = _gen_map2()

def _gen_map3():
    R,C=11,100
    m=[[' ']*C for _ in range(R)]
    def fill(r1,r2,c1,c2,ch='#'):
        for r in range(r1,r2):
            for c in range(c1,c2):
                if 0<=r<R and 0<=c<C: m[r][c]=ch
    fill(8,11,0,40); fill(8,11,76,100)
    m[6][1]='P'; m[7][8]='S'; m[7][25]='E'
    m[6][25]='A'; m[6][26]='A'; m[7][25]='A'; m[7][26]='A'
    fill(0,9,27,40)
    fill(0,1,40,75); fill(8,9,40,75); fill(0,9,40,41); fill(0,9,74,75)
    for c in [51,52,53,54,55]: m[1][c]='R'
    for c in [60,61,62,63,64,65]: m[1][c]='R'
    m[4][48]='$'
    m[6][41]='C'; m[6][42]='C'; m[7][41]='C'; m[7][42]='C'
    m[6][71]='B'; m[6][72]='B'; m[7][71]='B'; m[7][72]='B'
    fill(8,11,40,80); fill(0,8,73,82)
    fill(3,8,75,100); fill(8,11,75,100)
    m[1][82]='D'; m[1][83]='D'; m[2][82]='D'; m[2][83]='D'
    m[2][97]='*'; m[1][97]='*'; m[0][97]='*'
    return [''.join(r) for r in m]

MAP_3 = _gen_map3()

def _gen_map4():
    R,C=12,80
    m=[[' ']*C for _ in range(R)]
    def fill(r1,r2,c1,c2,ch='#'):
        for r in range(r1,r2):
            for c in range(c1,c2):
                if 0<=r<R and 0<=c<C: m[r][c]=ch
    fill(10,11,0,80)
    m[8][1]='P'; 
    fill(0,1,0,40); fill(0,7,0,1); fill(6,7,0,3); fill(6,7,4,40); fill(0,7,39,40)
    m[9][39]='*'; m[8][39]='*'; m[7][39]='*'
    m[1][1]='$'; m[4][20]='$'; m[1][38]='$'
    return [''.join(r) for r in m]

MAP_4 = _gen_map4()


def _gen_map6():
    R,C=11,100
    m=[[' ']*C for _ in range(R)]
    def fill(r1,r2,c1,c2,ch='#'):
        for r in range(r1,r2):
            for c in range(c1,c2):
                if 0<=r<R and 0<=c<C: m[r][c]=ch
    fill(8,12,0,5); fill(8,12,10,15); fill(8,12,20,25)
    fill(8,12,30,35); fill(8,12,40,45)
    m[6][1]='P'
    m[2][97]='*'
    fill(3,12,50,70)
    m[2][55]='*'; m[1][55]='*'; m[0][55]='*'
    return [''.join(r) for r in m]

MAP_6 = _gen_map6()

# Vị trí sao cho màn 6-9 (map thường)
VITRI_SAO = {
    6:  [(6,8),(5,25),(4,42)],
    7:  [(6,5),(5,35),(4,65)],
    8:  [(5,8),(6,28),(4,42)],
    9:  [(6,12),(5,35),(4,50)],
}
def _gen_map7():
    R,C=11,100
    m=[[' ']*C for _ in range(R)]
    def fill(r1,r2,c1,c2,ch='#'):
        for r in range(r1,r2):
            for c in range(c1,c2):
                if 0<=r<R and 0<=c<C: m[r][c]=ch
    fill(10,11,0,80);fill(0,11,0,1);fill(0,1,0,80);fill(0,11,79,80)
    m[9][2]='P'
    fill(3,6,1,3)
    m[2][2]='$'
    fill(3,4,3,5)
    fill(8,10,7,9);fill(3,4,7,9)
    fill(4,7,12,14)
    
    return [''.join(r) for r in m]

MAP_7 = _gen_map7()

def _gen_map8():
    # Khung tạm — chưa thiết kế
    R,C=11,40
    m=[[' ']*C for _ in range(R)]
    def fill(r1,r2,c1,c2,ch='#'):
        for r in range(r1,r2):
            for c in range(c1,c2):
                if 0<=r<R and 0<=c<C: m[r][c]=ch
    fill(10,11,0,40); fill(0,11,0,1); fill(0,1,0,40); fill(0,11,39,40)
    fill(8,10,1,10)
    m[7][2]='P'
    m[5][20]='$'; m[5][30]='$'; m[5][35]='$'
    fill(3,5,35,39); m[2][37]='*'
    return [''.join(r) for r in m]

MAP_8 = _gen_map8()

def _gen_map9():
    # Khung tạm — chưa thiết kế
    R,C=11,40
    m=[[' ']*C for _ in range(R)]
    def fill(r1,r2,c1,c2,ch='#'):
        for r in range(r1,r2):
            for c in range(c1,c2):
                if 0<=r<R and 0<=c<C: m[r][c]=ch
    fill(10,11,0,40); fill(0,11,0,1); fill(0,1,0,40); fill(0,11,39,40)
    fill(8,10,1,10)
    
    m[7][2]='P'
    m[5][20]='$'; m[5][30]='$'; m[5][35]='$'
    fill(3,5,35,39); m[2][37]='*'
    return [''.join(r) for r in m]

MAP_9 = _gen_map9()

def _gen_map_boss5():
    R,C=11,40
    m=[[' ']*C for _ in range(R)]
    def fill(r1,r2,c1,c2,ch='#'):
        for r in range(r1,r2):
            for c in range(c1,c2):
                if 0<=r<R and 0<=c<C: m[r][c]=ch
    fill(10,11,0,40)   # sàn
    fill(0,11,0,1)     # tường trái
    m[3][39]='E';m[6][39]='E'
    fill(0,11,39,40)   # tường phải
    # Spawn + sao
    m[9][2]='P'
    m[5][10]='$'; m[5][20]='$'; m[5][30]='$'
    return [''.join(r) for r in m]

MAP_BOSS_5  = _gen_map_boss5()
MAP_BOSS_10 = _gen_map_boss5()   # boss10 dùng cùng layout với boss5

def _lay_map(n):
    if   n==1:  return MAP_1,False
    elif n==2:  return MAP_2,False
    elif n==3:  return MAP_3,False
    elif n==4:  return MAP_4,False
    elif n==5:  return MAP_BOSS_5,True
    elif n==6:  return MAP_6,False
    elif n==7:  return MAP_7,False
    elif n==8:  return MAP_8,False
    elif n==9:  return MAP_9,False
    elif n==10: return MAP_BOSS_10,True
    return MAP_1,False

class _SaoMap(pygame.sprite.Sprite):
    def __init__(self,c,r):
        super().__init__()
        S=TILE_SIZE
        self._dem=0
        self._s=S
        self.image=pygame.Surface((S,S),pygame.SRCALPHA)
        self.rect=self.image.get_rect(topleft=(c*S,r*S))
        self._ve()
    def _ve(self):
        import math
        S=self._s; cx=cy=S//2
        pts=[]
        for i in range(10):
            a=math.radians(-90+i*36); ri=cx-4 if i%2==0 else cx//2
            pts.append((cx+ri*math.cos(a),cy+ri*math.sin(a)))
        self.image.fill((0,0,0,0))
        pygame.draw.polygon(self.image,(255,215,0),pts)
        pygame.draw.polygon(self.image,(255,255,120),pts,2)
    def update(self):
        import math
        self._dem+=1
        a=int(180+75*abs(math.sin(self._dem*0.06)))
        self.image.set_alpha(a)

# ══════════════════════════════════════════════════════════
#  VIDEO TOÀN MÀN HÌNH
# ══════════════════════════════════════════════════════════
class VideoIntro:
    def __init__(self):
        self.hien=False; self._rs=None; self.ft=self.fn=None
    def _init(self,h):
        if not self.ft:
            self.ft=pygame.font.SysFont(FONT_CHINH,max(26,h//16),bold=True)
            self.fn=pygame.font.SysFont(FONT_CHINH,max(15,h//30))
    def bat(self): self.hien=True
    def ve(self,screen):
        if not self.hien: return
        w,h=screen.get_size(); self._init(h)
        ov=pygame.Surface((w,h),pygame.SRCALPHA); ov.fill((0,0,0,225))
        screen.blit(ov,(0,0))
        VW,VH=int(w*.72),int(h*.68); vx,vy=(w-VW)//2,(h-VH)//2
        pygame.draw.rect(screen,(12,12,12),(vx,vy,VW,VH),border_radius=10)
        pygame.draw.rect(screen,(65,65,80),(vx,vy,VW,VH),2,border_radius=10)
        t1=self.ft.render("▶  VIDEO GIỚI THIỆU",True,(165,165,178))
        t2=self.fn.render("(Chưa có nội dung — sẽ cập nhật sau)",True,(95,95,108))
        screen.blit(t1,t1.get_rect(center=(vx+VW//2,vy+VH//2-18)))
        screen.blit(t2,t2.get_rect(center=(vx+VW//2,vy+VH//2+22)))
        sw,sh=130,34; sx=vx+VW-sw-12; sy=vy+VH-sh-12
        self._rs=pygame.Rect(sx,sy,sw,sh)
        mx,my=pygame.mouse.get_pos(); hv=self._rs.collidepoint(mx,my)
        pygame.draw.rect(screen,(55,55,80) if hv else(30,30,50),self._rs,border_radius=7)
        pygame.draw.rect(screen,(110,110,160),self._rs,1,border_radius=7)
        ts=self.fn.render("Bo qua  >>",True,(200,200,222))
        screen.blit(ts,ts.get_rect(center=self._rs.center))
    def xu_ly(self,ev):
        if not self.hien: return False
        if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
            if self._rs and self._rs.collidepoint(ev.pos): self.hien=False; return True
        if ev.type==pygame.KEYDOWN and ev.key in(pygame.K_ESCAPE,pygame.K_RETURN,pygame.K_SPACE):
            self.hien=False; return True
        return False

# ══════════════════════════════════════════════════════════
#  MÀN CHƠI
# ══════════════════════════════════════════════════════════
class ManChoi:
    def __init__(self,man_hinh):
        self.man_hinh=man_hinh; self.so_man=1
        self.am_bat=True; self.tam_dung=False; self.muc_pause=0; self.da_thang=False
        self.video=VideoIntro(); self.tinh_linh=TinhLinh()
        self.hud=HUD()
        self.ket_qua=ManKetQua()
        self.co_kiem=False
        self.co_hoan_doi=False
        self.da_co_dash=False
        self._giap_active=False
        self._giap_timer=0
        self._giap_cd=0
        self.GIAP_TGIAN=60
        self.GIAP_CD=600
        self._ds_cau=pygame.sprite.Group()  # group quả cầu boss
        self._i_frames=0    # bất tử tạm sau khi bị đẩy   # đã mở khóa dash chưa (giữ qua màn)   # kỹ năng hoán đổi
        self._dang_la_tinh_linh=False   # đang điều khiển tinh linh
        self._tl_dieu_khien=None   # TinhLinhDieuKhien instance
        self._nhan_vat_goc_pos=(0,0)   # vị trí nhân vật khi hoán đổi
        # Hội thoại vật phẩm (kiếm/sách)
        self._thoai_vatpham      = False   # đang hiện thoại
        self._thoai_vatpham_noi  = "(Hoi thoai trong — se cap nhat sau)" 
        self._tao_font(); self._tai_ban_do()

    def _tao_font(self):
        w,h=self.man_hinh.get_size()
        self.ft=pygame.font.SysFont(FONT_CHINH,max(30,h//12),bold=True)
        self.fm=pygame.font.SysFont(FONT_CHINH,max(18,h//24),bold=True)
        self.fn=pygame.font.SysFont(FONT_CHINH,max(13,h//36))

    def tai_man(self,n):
        self.so_man=n; self.da_thang=False; self.tam_dung=False
        self.tinh_linh=TinhLinh()
        self.hud.reset()
        self.ket_qua.an()   # ẩn overlay thắng/thua khi vào màn mới
        if n<=2: self.co_kiem=False
        self.co_hoan_doi = (n >= 4) and (n not in (6,7,8,9))
        self._dang_la_tinh_linh=False
        self._tl_dieu_khien=None
        self._boss_win=False
        self._boss_timer=0
        self._tai_ban_do()   # tạo NhanVat mới ở đây
        # Màn 3: dash chỉ có nếu đã nhặt sách
        # Màn 4+: luôn có dash
        if n >= 4:       self.nhan_vat.co_dash = True;  self.da_co_dash = True
        elif n == 3:     self.nhan_vat.co_dash = self.da_co_dash
        else:            self.nhan_vat.co_dash = False
        if n==1: self.video.bat()

    def _tai_ban_do(self):
        ban_do,la_boss=_lay_map(self.so_man)
        self.ban_do=ban_do; self.la_boss=la_boss
        Tile=NenTangBoss if la_boss else NenTang
        self.ds_nen     =pygame.sprite.Group()
        self.ds_vat     =pygame.sprite.Group()
        self.ds_dich    =pygame.sprite.Group()
        self.ds_kiem    =pygame.sprite.Group()
        self.ds_ke      =pygame.sprite.Group()
        self.ds_sach    =pygame.sprite.Group()
        self.ds_dc      =pygame.sprite.Group()
        self.ds_sao_map =pygame.sprite.Group()
        self.ds_roi     =pygame.sprite.Group()
        self.ds_boss    =pygame.sprite.Group()
        self._ds_cau    =pygame.sprite.Group()
        self.ds_nuoc      = pygame.sprite.Group()
        self._ds_kiem_nem = pygame.sprite.Group()
        self._ds_kiem_bay = pygame.sprite.Group()   # dùng ở mọi màn (tránh crash)
        self._ds_kiem_mua = pygame.sprite.Group()   # dùng ở mọi màn
        self._i_frames  =0
        self._boss_timer= 0    # đếm frame
        self._boss_win  = False
        sx=sy=0
        for ri,hang in enumerate(ban_do):
            for ci,o in enumerate(hang):
                if   o=='#': self.ds_nen.add(Tile(ci,ri))
                elif o=='W': self.ds_vat.add(KhucGo(ci,ri))
                elif o=='K': self.ds_kiem.add(Kiem(ci,ri,ngang=False))
                elif o=='S': self.ds_sach.add(Sach1x1(ci,ri))
                elif o=='~': self.ds_nuoc.add(KhoiNuoc(ci,ri))
                # Cổng A: khu2→khu3
                elif o=='A' and ri==6 and ci==25: self.ds_dc.add(KhoiDichChuyen(ci,ri,41,6))
                # Cổng C: khu3→khu2 (chiều ngược A)
                elif o=='C' and ri==6 and ci==41: self.ds_dc.add(KhoiDichChuyen(ci,ri,35,6))
                # Cổng B: khu3→khu4
                elif o=='B' and ri==6 and ci==71: self.ds_dc.add(KhoiDichChuyen(ci,ri,82,1))
                # Cổng D: khu4→khu3 (chiều ngược B)
                elif o=='D' and ri==1 and ci==82: self.ds_dc.add(KhoiDichChuyen(ci,ri,71,6))
                elif o=='E':
                    co_tc = self.so_man in (6,7,8,9)
                    self.ds_ke.add(KeDiChuyen(ci,ri,20,40, co_tan_cong=co_tc))
                elif o=='$': self.ds_sao_map.add(_SaoMap(ci,ri))
                elif o=='R': self.ds_roi.add(KhoiRoi(ci,ri,ngang=False))
                elif o=='r': self.ds_roi.add(KhoiRoi(ci,ri,ngang=True))
                elif o=='P': sx,sy=ci,ri
                elif o=='*': self.ds_dich.add(ODict(ci,ri))
        # Thêm sao cho map dùng VITRI_SAO
        if self.so_man in VITRI_SAO and len(self.ds_sao_map)==0:
            for (sr,sc) in VITRI_SAO[self.so_man]:
                self.ds_sao_map.add(_SaoMap(sc,sr))
        self.nhan_vat=NhanVat(sx*T,sy*T)
        self.nhan_vat.so_kiem = 0   # reset kiếm nhặt mỗi màn
        self.spawn_pos=(sx*T,sy*T)
        # Spawn boss tại row=8, col=37
        if self.so_man==5:
            self.ds_boss.add(Boss5(37,8))
        elif self.so_man==10:
            self.ds_boss.add(Boss10(37,8))
        # Skill vars chung cho man5 và man10 — reset mỗi lần tải màn boss
        if self.so_man in (5,10):
            self._bsk_sk1_next   = 5*FPS
            self._bsk_sk2_done   = False
            self._bsk_sk2_active = False
            self._bsk_sk2_timer  = 0
            self._bsk_khoi_an    = []
        # Vars riêng boss10
        if self.so_man == 10:
            self._b10_phase     = 1
            self._b10_hp        = 10
            self._b10_sk1_count = 0
            self._b10_sk1_next  = 5*FPS
            self._b10_sk2_phase = False
            self._b10_sk3_queue = 0
            self._b10_sk3_timer = 0
            self._b10_sk3_count = 0        # đếm số lần đã dùng SK3
            self._b10_teleported= False
            self._ds_kiem_bay   = pygame.sprite.Group()
            self._ds_kiem_mua   = pygame.sprite.Group()
            # SK4 vars
            self._b10_sk4_active = False   # đang thi triển SK4
            self._b10_sk4_dem    = 0       # frame đã chạy
            self._b10_sk4_sokem  = 0       # tổng số kiếm cần spawn
            self._b10_sk4_spawned= 0       # số đã spawn
            # Bị động phase2: né + phản công khi player dash vào
            self._b10_bd_active = True   # cơ chế đang bật
            self._b10_bd_cd     = 0      # cooldown 5s sau SK1
            self._b10_bd_ne     = 0      # đang lướt lùi (frame còn lại)
            self._b10_bd_ne_dir = 1      # hướng lùi
        # ds_dich đã được load trong vòng for
        rong=len(ban_do[0])*T; cao=len(ban_do)*T
        self.camera=Camera(rong,cao)
        if self.so_man==1:
            self.tinh_linh.bat_dau(sx*T+T*3,sy*T)
            self.tinh_linh.dat_trigger(10*T,"(Hoi thoai trong — se cap nhat sau)")
        elif self.so_man==2:
            self.tinh_linh.bat_dau(sx*T+T*2,sy*T)
            self.tinh_linh.dat_trigger(5*T,"Ta la tinh linh! Double-click de ta bay toi do va lam be dung!")
        elif self.so_man==3:
            self.tinh_linh.bat_dau(sx*T+T*2,sy*T)
            self.tinh_linh.dat_trigger(5*T,"Nhat sach de mo khoa ky nang Dash! Nhan Shift de luot!")
        elif self.so_man==4:
            self.tinh_linh.bat_dau(sx*T+T*2,sy*T)
            self.tinh_linh.dat_trigger(8*T,"Nhan Q de hoan doi voi ta! Ta se bay qua duoc chuong ngai!")
            self.co_hoan_doi=True
        elif self.so_man in (5,10):
            # Boss: tinh linh có mặt nhưng không hoán đổi
            self.tinh_linh.bat_dau(sx*T+T*2,sy*T)
        # Màn 6-9: không có tinh linh

    def _hoi_sinh(self):
        self.nhan_vat.rect.topleft=self.spawn_pos
        self.nhan_vat.vel_y=self.nhan_vat.vel_x=0

    # ── Boss skill helpers (dùng chung cho man5 và man10) ─
    def _boss_sk1_ban(self):
        """Skill 1: bắn 5 quả cầu từ boss hướng về player."""
        for b in self.ds_boss:
            bx,by = b.rect.centerx, b.rect.centery
            px,py = self.nhan_vat.rect.centerx, self.nhan_vat.rect.centery
            for ox in (-40,-20,0,20,40):
                self._ds_cau.add(QuaCau(bx+ox, by, px, py))

    def _boss_an_khoi(self, toan_bo_san=False):
        """Skill 2: ẩn tile.
        toan_bo_san=True  → xóa toàn bộ sàn row cuối (boss10).
        toan_bo_san=False → chỉ xóa platform dưới chân (boss5)."""
        map_h  = len(self.ban_do)
        map_w  = max(len(r) for r in self.ban_do) if self.ban_do else 40
        san_y  = (map_h - 1) * T
        bien_p = (map_w - 1) * T

        hidden = []
        if toan_bo_san:
            # Boss10: xóa TẤT CẢ tile ở row sàn (fill(10,11,0,40))
            for tile in list(self.ds_nen):
                if abs(tile.rect.y - san_y) <= T // 4:
                    hidden.append(tile)
        else:
            # Boss5: platform trực tiếp dưới chân, loại biên
            px_l = self.nhan_vat.rect.left
            px_r = self.nhan_vat.rect.right
            py_b = self.nhan_vat.rect.bottom
            for tile in list(self.ds_nen):
                if tile.rect.x <= 0:          continue
                if tile.rect.right >= bien_p: continue
                if tile.rect.y <= 0:          continue
                if tile.rect.y >= san_y:      continue
                if abs(tile.rect.top - py_b) <= T // 2:
                    if tile.rect.right > px_l and tile.rect.left < px_r:
                        hidden.append(tile)

        for tile in hidden:
            self.ds_nen.remove(tile)
        self._bsk_khoi_an    = hidden
        self._bsk_sk2_active = True
        self._bsk_sk2_timer  = 5 * FPS

    def _boss_hien_khoi(self):
        """Restore tile đã ẩn bởi skill 2."""
        for tile in getattr(self,'_bsk_khoi_an',[]):
            self.ds_nen.add(tile)
        self._bsk_khoi_an    = []
        self._bsk_sk2_active = False
        self._bsk_sk2_timer  = 0

    # ── Boss10 helpers ─────────────────────────────────────
    def _b10_ban_cau(self):
        """SK1 boss10: bắn 5 cầu phân tán."""
        for b in self.ds_boss:
            bx,by=b.rect.centerx,b.rect.centery
            px,py=self.nhan_vat.rect.centerx,self.nhan_vat.rect.centery
            for ox in (-40,-20,0,20,40):
                self._ds_cau.add(QuaCau(bx+ox,by,px,py))

    def _b10_bat_dau_sk3(self):
        """SK3: boss teleport tới player rồi chém kiếm.
        Phase1: lần 4 → SK4 (10 kiếm).
        Phase2: lần 3 → SK4 (20 kiếm)."""
        self._b10_sk3_count += 1
        nguong_sk4 = 1 if self._b10_phase == 2 else 2

        if self._b10_sk3_count >= nguong_sk4:
            self._b10_sk3_count = 0
            self._b10_bat_dau_sk4()
            return

        b = next(iter(self.ds_boss), None)
        if not b: return
        px, py = self.nhan_vat.rect.centerx, self.nhan_vat.rect.centery
        offset = TILE_SIZE*2 + b.rect.width//2
        b.rect.centerx = px + offset
        b.rect.bottom  = self.nhan_vat.rect.bottom
        lans = 3 if self._b10_phase == 2 else 1
        self._b10_sk3_queue = lans
        self._b10_sk3_timer = 1
        self._b10_chem_kiem()
        self._b10_sk3_queue -= 1

    def _b10_chem_kiem(self):
        """Spawn kiếm bay từ boss về hướng player."""
        b = next(iter(self.ds_boss), None)
        if not b: return
        bx,by = b.rect.centerx, b.rect.centery
        px,py = self.nhan_vat.rect.centerx, self.nhan_vat.rect.centery
        dx = px-bx; dy = py-by
        self._ds_kiem_bay.add(
            KiemBay(bx, by, dx, dy, phase=self._b10_phase))

    def _b10_bat_dau_sk4(self):
        """SK4: mưa kiếm từ trên phải→trái, 5s hiện hết, tracking player."""
        so_kem = 20 if self._b10_phase == 2 else 10
        self._b10_sk4_active  = True
        self._b10_sk4_dem     = 0
        self._b10_sk4_sokem   = so_kem
        self._b10_sk4_spawned = 0

    def _b10_phan_cong(self):
        """Bị động phase2: phản công SK3 + 1 kiếm ngang + 1 kiếm dọc ngay."""
        b = next(iter(self.ds_boss), None)
        if not b: return
        bx, by = b.rect.centerx, b.rect.centery
        px, py = self.nhan_vat.rect.centerx, self.nhan_vat.rect.centery
        # 1 kiếm hướng thẳng về player
        dx = px - bx; dy = py - by
        self._ds_kiem_bay.add(KiemBay(bx, by, dx, dy, phase=2))
        # 1 kiếm vuông góc (ngang nếu player lệch dọc, dọc nếu lệch ngang)
        if abs(dx) >= abs(dy):
            self._ds_kiem_bay.add(KiemBay(bx, by, 0, 1, phase=2))   # dọc
        else:
            self._ds_kiem_bay.add(KiemBay(bx, by, 1, 0, phase=2))   # ngang
        # Cũng kích SK3 ngay (3 lần chém)
        self._b10_sk3_queue = 3
        self._b10_sk3_timer = 12

    def _teleport(self, dest_x, dest_y):
        self.nhan_vat.rect.topleft = (dest_x, dest_y)
        self.nhan_vat.vel_y = 0; self.nhan_vat.vel_x = 0
        # Tinh linh dịch chuyển tức thì cùng nhân vật
        if self.tinh_linh.hien:
            self.tinh_linh.x = float(dest_x + TILE_SIZE)
            self.tinh_linh.y = float(dest_y)
            self.tinh_linh._dang_di_chuyen = False
            self.tinh_linh.la_platform     = False

    def _ve_thoai_vatpham(self, w, h):
        """Overlay hội thoại sau khi nhặt vật phẩm."""
        BW,BH=360,90
        bx=(w-BW)//2; by=h-BH-60
        bong=pygame.Surface((BW,BH),pygame.SRCALPHA)
        pygame.draw.rect(bong,(15,15,35,235),(0,0,BW,BH),border_radius=10)
        pygame.draw.rect(bong,(180,140,60,255),(0,0,BW,BH),2,border_radius=10)
        self.man_hinh.blit(bong,(bx,by))
        t1=self.fm.render("Nhat duoc vat pham!",True,VANG)
        t2=self.fn.render(self._thoai_vatpham_noi,True,TRANG)
        t3=self.fn.render("[F] Dong",True,XAM)
        self.man_hinh.blit(t1,t1.get_rect(center=(bx+BW//2,by+24)))
        self.man_hinh.blit(t2,t2.get_rect(center=(bx+BW//2,by+50)))
        self.man_hinh.blit(t3,(bx+BW-t3.get_width()-10,by+BH-t3.get_height()-6))

    def update(self):
        self._tao_font()
        if self.tam_dung: return
        if self.ket_qua.hien: return   # đang hiện kết quả
        self.nhan_vat.khoa(self.video.hien or self._dang_la_tinh_linh)
        # Cập nhật giáp bất tử
        if self._giap_cd > 0: self._giap_cd -= 1
        if self._giap_active:
            self._giap_timer -= 1
            if self._giap_timer <= 0:
                self._giap_active = False

        # Cập nhật tinh linh điều khiển
        if self._dang_la_tinh_linh and self._tl_dieu_khien:
            self._tl_dieu_khien.update(list(self.ds_nen)+list(self.ds_vat))

        # Xây danh sách va chạm (thêm tinh linh nếu là platform)
        tat_ca=list(self.ds_nen)+list(self.ds_vat)
        if self.tinh_linh.hien and self.tinh_linh.la_platform:
            tl_rect=self.tinh_linh.rect   # property trả về pygame.Rect
            if tl_rect:
                class _P:
                    def __init__(self,r): self.rect=r
                tat_ca.append(_P(tl_rect))

        # Không leo khi đang có hội thoại mở
        co_thoai_mo = self._thoai_vatpham or any(dc._cho_tra_loi for dc in self.ds_dc)
        chuot_giu = pygame.mouse.get_pressed()[0] and not self.video.hien and not co_thoai_mo
        self.nhan_vat.kiem_tra_co_the_leo(tat_ca)
        # ── Phát hiện nhân vật trong nước ─────────────────
        self.nhan_vat.trong_nuoc = any(
            self.nhan_vat.rect.colliderect(n.rect) for n in self.ds_nuoc)
        self.nhan_vat.update(tat_ca, chuot_trai_giu=chuot_giu)
        self.ds_nuoc.update()

        # ── Nhặt kiếm mưa đang nằm dưới đất ─────────────
        for k in list(self._ds_kiem_mua):
            if k.co_the_nhat(self.nhan_vat.rect):
                self.nhan_vat.so_kiem += 1
                k.kill()

        # ── Ném kiếm (F) ──────────────────────────────────
        self._ds_kiem_nem.update(list(self.ds_nen)+list(self.ds_vat))
        if self.nhan_vat._nem_signal:
            cx = self.nhan_vat.rect.centerx
            cy = self.nhan_vat.rect.centery
            self._ds_kiem_nem.add(
                KiemNem(cx, cy, self.nhan_vat.huong))

        # ── Kiếm ném chạm boss ────────────────────────────
        for kn in list(self._ds_kiem_nem):
            for b in list(self.ds_boss):
                if kn.cham_boss(b.rect):
                    kn.kill()
                    if hasattr(b, 'nhan_don'):
                        b.nhan_don()
                    break
        self.tinh_linh.update(self.nhan_vat.rect, list(self.ds_nen)+list(self.ds_vat))
        if self._dang_la_tinh_linh and self._tl_dieu_khien:
            self.camera.cap_nhat_vi_tri(
                self._tl_dieu_khien.rect.centerx,
                self._tl_dieu_khien.rect.centery)
        else:
            self.camera.cap_nhat(self.nhan_vat)
        self.ds_kiem.update()
        # Truyền player_rect để quái có thể tấn công
        for ke in self.ds_ke:
            ke.update(list(self.ds_nen), player_rect=self.nhan_vat.rect)
        # Quái tấn công người chơi (va chạm trực tiếp)
        if self._i_frames <= 0:
            for ke in list(self.ds_ke):
                hit, dx, dy = ke.kiem_tra_tan_cong(self.nhan_vat.rect, self._i_frames)
                if hit:
                    if 1 <= self.so_man <= 4:
                        self.nhan_vat.vel_y = -9
                        self._i_frames = KeDiChuyen.I_FRAMES
                        self.so_frame_day = 8
                        self.huong_day_lui = dx
                    elif 6 <= self.so_man <= 9:
                        go = self.hud.mat_mang()
                        if go: self.ket_qua.hien_thua(self.so_man)
                        else:
                            self.nhan_vat.vel_y = -9
                            self._i_frames = KeDiChuyen.I_FRAMES
                            self.so_frame_day = 8
                            self.huong_day_lui = dx
                    break

        # ── Đạn quái màn 6-9 chạm player ─────────────────
        if 6 <= self.so_man <= 9 and self._i_frames <= 0:
            for ke in list(self.ds_ke):
                if ke._dan is not None and ke._dan.cham_nguoi(self.nhan_vat.rect):
                    ke._dan._alive = False
                    go = self.hud.mat_mang()
                    if go: self.ket_qua.hien_thua(self.so_man)
                    else:  self._i_frames = KeDiChuyen.I_FRAMES
                    break
        
        # ==============================================================
        # Xử lý ép đẩy lùi vật lý
        if hasattr(self, 'so_frame_day') and self.so_frame_day > 0:
            self.so_frame_day -= 1
            # SỬA Ở ĐÂY: Chỉ lùi 1 pixel mỗi frame
            # Tổng cộng lùi: 8 frame * 1 pixel = 8 pixel 
            self.nhan_vat.rect.x += self.huong_day_lui * 1

        if self._i_frames > 0: self._i_frames -= 1
        # Boss10 auto-bắn cầu (boss5 dùng skill riêng)
        nen_vat = list(self.ds_nen) + list(self.ds_vat)
        for c in self._ds_cau: c.update(nen_vat)
        self.ds_sach.update()
        self.ds_dc.update()
        # Cổng dịch chuyển — xử lý hội thoại
        for dc in self.ds_dc:
            dc.xu_ly_vung(self.nhan_vat.rect)
        self.ds_boss.update()
        self.ds_sao_map.update()
        # ══════════════════ BOSS 5 LOGIC ══════════════════
        if self.so_man == 5 and self.ds_boss:
            self._boss_timer += 1
            bt = self._boss_timer

            # ── Skill 1: từ giây 5, mỗi 10s bắn 5 cầu ──────
            if bt == self._bsk_sk1_next:
                self._boss_sk1_ban()
                self._bsk_sk1_next += 10 * FPS

            # ── Skill 2: giây 30, ẩn khối dưới chân 5s ──────
            if bt == 30*FPS and not self._bsk_sk2_done:
                self._bsk_sk2_done = True
                self._boss_an_khoi()

            if self._bsk_sk2_active:
                self._bsk_sk2_timer -= 1
                if self._bsk_sk2_timer <= 0:
                    self._boss_hien_khoi()

            # ── Cầu skill1 chạm player ────────────────────
            if self._i_frames <= 0:
                for c in list(self._ds_cau):
                    if c.cham_nguoi(self.nhan_vat.rect) and not self._giap_active:
                        c.kill()
                        go = self.hud.mat_mang()
                        if go:
                            self._boss_hien_khoi()
                            self.ket_qua.hien_thua(self.so_man)
                        else:
                            self._i_frames = 5*FPS
                        break

            # ── Chạm boss → bất tử 5s tại chỗ ───────────
            for b in self.ds_boss:
                if b.cham_nguoi(self.nhan_vat.rect) \
                        and self._i_frames <= 0 and not self._giap_active:
                    go = self.hud.mat_mang()
                    if go:
                        self._boss_hien_khoi()
                        self.ket_qua.hien_thua(self.so_man)
                    else:
                        self._i_frames = 5*FPS
                    break

            # ── Sống sót 60s → thắng ──────────────────────
            if bt >= 60*FPS and not self.ket_qua.hien:
                self._boss_hien_khoi()
                self._boss_win = True; self.da_thang = True
                self.ket_qua.hien_thang(self.so_man, self.hud.sao)

        # ════════════════ BOSS 10 LOGIC ═══════════════════
        elif self.so_man == 10:
            self._boss_timer += 1
            bt = self._boss_timer

            # ── Hết 120s → player thua luôn ─────────────
            if bt >= 120*FPS and not self.ket_qua.hien:
                self._boss_hien_khoi()
                while self.hud.tim > 0:
                    self.hud.mat_mang()
                self.ket_qua.hien_thua(self.so_man)

            # ─── Update kiếm bay ─────────────────────────
            nen_vat = list(self.ds_nen) + list(self.ds_vat)
            self._ds_kiem_bay.update(nen_vat)

            # ─── Update SK4 kiếm mưa ─────────────────────
            self._ds_kiem_mua.update(nen_vat)

            if self._b10_sk4_active and \
                    self._b10_sk4_spawned < self._b10_sk4_sokem:
                self._b10_sk4_dem += 1
                interval = max(1, (5*FPS) // self._b10_sk4_sokem)
                if self._b10_sk4_dem % interval == 0:
                    map_w  = len(self.ban_do[0]) * T
                    idx    = self._b10_sk4_spawned
                    total  = self._b10_sk4_sokem
                    sx = int(map_w * (1.0 - idx/total)) - T//2
                    sx = max(T, min(sx, map_w - T))
                    k = KiemMua(sx, -T, phase=self._b10_phase)
                    k.dat_huong(self.nhan_vat.rect.centerx,
                                self.nhan_vat.rect.centery)
                    self._ds_kiem_mua.add(k)
                    self._b10_sk4_spawned += 1
                    if self._b10_sk4_spawned >= self._b10_sk4_sokem:
                        self._b10_sk4_active = False

            # ─── SK2 đang active (ẩn khối) ───────────────
            if self._b10_sk2_phase:
                self._bsk_sk2_timer -= 1
                if self._bsk_sk2_timer <= 0:
                    # Hết 5s: hồi khối, hồi HP, chuyển phase hoặc thắng
                    self._boss_hien_khoi()
                    self._b10_sk2_phase = False
                    if self._b10_phase == 1:
                        # Chuyển sang phase 2
                        self._b10_phase = 2
                        self._b10_hp    = 20
                        for b in self.ds_boss:
                            b.mau        = 20
                            b.SO_MAU_MAX = 20
                        # Reset SK1 và SK3 counter — tính từ frame HIỆN TẠI (sau SK2)
                        self._b10_sk1_next  = bt + 5*FPS
                        self._b10_sk1_count = 0
                        self._b10_sk3_count = 0
                        self._b10_bd_active = True   # bật bị động phase2
                    else:
                        # Phase 2 hết HP → thắng
                        self._boss_hien_khoi()
                        self._boss_win = True; self.da_thang = True
                        self.ket_qua.hien_thang(self.so_man, self.hud.sao)
            # ─── Dash chạm boss → trừ máu ────────────────
            if self.nhan_vat.dang_dash and self._i_frames <= 0:
                for b in list(self.ds_boss):
                    if self.nhan_vat.rect.colliderect(b.rect):
                        if hasattr(b, 'nhan_don'):
                            b.nhan_don()
                        break

            # ─── Bị động phase2: luôn bật, né khi dash vào ─


            # ─── Bị động phase2: né + phản công khi dash vào ─
            if self._b10_phase == 2 and not self._b10_sk2_phase:
                # Đếm cooldown bị động
                if self._b10_bd_cd > 0:
                    self._b10_bd_cd -= 1
                    if self._b10_bd_cd == 0:
                        self._b10_bd_active = True

                # Lướt lùi
                if self._b10_bd_ne > 0:
                    self._b10_bd_ne -= 1
                    for b in self.ds_boss:
                        b.rect.x += self._b10_bd_ne_dir * 6
                        b.rect.x = max(T, min(b.rect.x,
                                    len(self.ban_do[0])*T - T - b.rect.width))

                # Kiểm tra: player dash vào vùng 7×7 boss
                if self._b10_bd_active and self._b10_bd_ne <= 0 \
                        and self._b10_sk3_queue == 0 \
                        and self.nhan_vat.dang_dash:
                    b = next(iter(self.ds_boss), None)
                    if b and b.rect.inflate(3*T*2,3*T*2).colliderect(self.nhan_vat.rect):
                        px = self.nhan_vat.rect.centerx
                        self._b10_bd_ne_dir = 1 if b.rect.centerx > px else -1
                        self._b10_bd_ne     = 16
                        # Tắt tạm 5s
                        self._b10_bd_active = False
                        self._b10_bd_cd     = 2 * FPS
                        self._b10_phan_cong()


            # ─── SK3 đang chạy (spawn kiếm từng đợt) ────
            if self._b10_sk3_queue > 0:
                self._b10_sk3_timer -= 1
                if self._b10_sk3_timer <= 0:
                    self._b10_sk3_queue -= 1
                    self._b10_chem_kiem()
                    self._b10_sk3_timer = 20
                            # SK3 xong → bật lại bị động
                    if self._b10_sk3_queue == 0 and self._b10_phase == 2:
                        self._b10_bd_active = True
                        self._b10_bd_cd     = 0
    

            # ─── SK1 bình thường (chỉ khi không có SK2/SK3 đang chạy) ──
            elif not self._b10_sk2_phase and not self.ket_qua.hien \
                    and bt >= self._b10_sk1_next:
                self._b10_sk1_count += 1
                self._b10_ban_cau()
                sk1_cd = 5*FPS if self._b10_phase==2 else 10*FPS
                self._b10_sk1_next = bt + sk1_cd
                # Tắt bị động trong SK1, hẹn 5s bật lại
                if self._b10_phase == 2:
                    self._b10_bd_active = False
                    self._b10_bd_cd     = 5*FPS
                # Sau 2 lần SK1 → dùng SK3
                if self._b10_sk1_count >= 2:
                    self._b10_sk1_count = 0
                    self._b10_bat_dau_sk3()

            # ─── Boss bị kill hết HP → SK2 hoặc thắng ───
            for b in list(self.ds_boss):
                if b.da_chet() and not self._b10_sk2_phase:
                    if self._b10_phase == 1:
                        # Phase 1: hồi full HP, ngăn fade, trigger SK2 toàn sàn
                        b.mau    = 10
                        b.SO_MAU_MAX = 10
                        b._flash = 0
                        b.image  = b._surf.copy()
                        b.image.set_alpha(255)
                        self._b10_sk2_phase = True
                        self._boss_an_khoi(toan_bo_san=True)
                        self._bsk_sk2_timer = 5 * FPS
                    else:
                        # Phase 2: boss chết thật → thắng
                        if not self.ket_qua.hien:
                            self._boss_hien_khoi()
                            self._ds_cau.empty()
                            self._ds_kiem_bay.empty()
                            self._ds_kiem_mua.empty()
                            self._boss_win = True; self.da_thang = True
                            self.ket_qua.hien_thang(self.so_man, self.hud.sao)

            # ─── Cầu chạm player ─────────────────────────
            if self._i_frames <= 0:
                for c in list(self._ds_cau):
                    if c.cham_nguoi(self.nhan_vat.rect) and not self._giap_active:
                        c.kill()
                        go = self.hud.mat_mang()
                        if go:
                            self._boss_hien_khoi()
                            self.ket_qua.hien_thua(self.so_man)
                        else:
                            self._i_frames = 5*FPS
                        break

                # ─── Kiếm bay chạm player ─────────────────
                for k in list(self._ds_kiem_bay):
                    if k.cham_nguoi(self.nhan_vat.rect) and not self._giap_active:
                        k.kill()
                        go = self.hud.mat_mang()
                        if go:
                            self._boss_hien_khoi()
                            self.ket_qua.hien_thua(self.so_man)
                        else:
                            self._i_frames = 5*FPS
                        break

                # ─── Kiếm mưa chạm player ─────────────────
                for k in list(self._ds_kiem_mua):
                    if k.cham_nguoi(self.nhan_vat.rect) and not self._giap_active:
                        k.kill()
                        go = self.hud.mat_mang()
                        if go:
                            self._boss_hien_khoi()
                            self.ket_qua.hien_thua(self.so_man)
                        else:
                            self._i_frames = 5*FPS
                        break

            # ─── Chạm boss → bất tử 5s ───────────────────
            for b in list(self.ds_boss):
                if b.cham_nguoi(self.nhan_vat.rect) and not self._giap_active \
                        and self._i_frames <= 0:
                    go = self.hud.mat_mang()
                    if go:
                        self._boss_hien_khoi()
                        self.ket_qua.hien_thua(self.so_man)
                    else:
                        self._i_frames = 5*FPS
                    break
        # Tinh linh nhặt sao khi đang điều khiển
        if self._dang_la_tinh_linh and self._tl_dieu_khien:
            nhat_tl = pygame.sprite.spritecollide(
                type('_R', (), {'rect': self._tl_dieu_khien.rect})(),
                self.ds_sao_map, True)
            for _ in nhat_tl: self.hud.nhat_sao()
        # Khối rơi
        self.ds_roi.update(list(self.ds_nen)+list(self.ds_vat))
        for kr in list(self.ds_roi):
            if kr.kiem_tra_cham_nguoi(self.nhan_vat.rect):
                kr.bat_dau_bien_mat()
                game_over = self.hud.mat_mang()
                if game_over: self.ket_qua.hien_thua(self.so_man)
                else:         self._hoi_sinh()
        # Nhặt sao
        nhat=pygame.sprite.spritecollide(self.nhan_vat,self.ds_sao_map,True)
        for _ in nhat: self.hud.nhat_sao()
        # Rơi xuống đáy → mất mạng
        if self.nhan_vat.rect.top > len(self.ban_do)*T + 50:
            if self.so_man in (5,10):
                # Rơi do SK2 (sàn biến mất) → restore + hồi sinh spawn + bất tử 5s
                self._boss_hien_khoi()
                go = self.hud.mat_mang()
                if go: self.ket_qua.hien_thua(self.so_man)
                else:
                    self._hoi_sinh()
                    self._i_frames = 5*FPS
            else:
                game_over = self.hud.mat_mang()
                if game_over: self.ket_qua.hien_thua(self.so_man)
                else: self._hoi_sinh()
        # Chạm đích → thắng
        if pygame.sprite.spritecollide(self.nhan_vat,self.ds_dich,False):
            self.da_thang=True
            self.ket_qua.hien_thang(self.so_man,self.hud.sao)

    def ve(self):
        w,h=self.man_hinh.get_size()
        self.man_hinh.fill((35,15,15) if self.la_boss else(90,165,245))
        cam=self.camera
        for s in[*self.ds_nen,*self.ds_dich,*self.ds_vat,*self.ds_kiem,*self.ds_ke,*self.ds_sach,*self.ds_dc,*self.ds_roi]:
            self.man_hinh.blit(s.image,cam.ap_dung(s))
        # Vẽ đạn quái (màn 6-9) + hiệu ứng tụ lực
        for ke in self.ds_ke:
            if ke._dan is not None and ke._dan._alive:
                dr = ke._dan.rect.move(-cam.lech_x, -cam.lech_y)
                self.man_hinh.blit(ke._dan.image, dr)
            # Khối tụ lực trên đầu khi đang chuẩn bị bắn
            if ke._sk_phase == 1:
                import math as _m
                prog = ke._tu_luc_dem / ke.TU_LUC_TIME
                T2 = TILE_SIZE
                bx = ke.rect.centerx - T2//2 - cam.lech_x
                by = ke.rect.top - T2 - 4 - cam.lech_y
                s2 = pygame.Surface((T2,T2), pygame.SRCALPHA)
                a2 = int(100 + 155*prog)
                pygame.draw.rect(s2,(220,60,60,a2),(0,0,T2,T2),border_radius=6)
                pygame.draw.rect(s2,(255,100,100,255),(0,0,T2,T2),2,border_radius=6)
                # Glow nhấp nháy
                rg = int(T2//2 * prog)
                if rg > 2:
                    g2 = pygame.Surface((rg*2,rg*2),pygame.SRCALPHA)
                    pygame.draw.circle(g2,(255,80,80,80),(rg,rg),rg)
                    self.man_hinh.blit(g2,(bx+T2//2-rg, by+T2//2-rg))
                self.man_hinh.blit(s2,(bx,by))
        # Vẽ nước (bán trong suốt, vẽ sau đất để overlay)
        for n in self.ds_nuoc:
            self.man_hinh.blit(n.image, cam.ap_dung(n))
        self.man_hinh.blit(self.nhan_vat.image,cam.ap_dung(self.nhan_vat))
        # Hiệu ứng giáp bất tử
        if self._giap_active:
            import math
            nr = self.nhan_vat.rect
            sx = nr.centerx - cam.lech_x
            sy = nr.centery - cam.lech_y
            r  = int(nr.width*0.8 + 4*math.sin(self._giap_timer*0.3))
            gs = pygame.Surface((r*2,r*2), pygame.SRCALPHA)
            a  = int(80 + 60*abs(math.sin(self._giap_timer*0.15)))
            pygame.draw.circle(gs,(100,220,255,a),(r,r),r)
            pygame.draw.circle(gs,(200,240,255,int(a*0.6)),(r,r),r,3)
            self.man_hinh.blit(gs,(sx-r,sy-r))
        if self._dang_la_tinh_linh and self._tl_dieu_khien:
            # Đang điều khiển tinh linh: chỉ vẽ tinh linh điều khiển
            self._tl_dieu_khien.ve(self.man_hinh, cam.lech_x, cam.lech_y)

        # Hint sách
        for s in self.ds_sach:
            if s.gan_nguoi_choi(self.nhan_vat.rect) and not s._bien_mat:
                s.ve_hint(self.man_hinh,cam.lech_x,cam.lech_y,self.fn)
        # Hội thoại cổng dịch chuyển
        for dc in self.ds_dc:
            dc.ve_hoi_thoai(self.man_hinh,cam.lech_x,cam.lech_y,w,h)
        # Hint kiếm
        for k in self.ds_kiem:
            if k.gan_nguoi_choi(self.nhan_vat.rect) and not k._bien_mat:
                k.ve_hint(self.man_hinh,cam.lech_x,cam.lech_y,self.fn)

        # Hint kẻ
        for ke in self.ds_ke:
            if ke.gan_nguoi_choi(self.nhan_vat.rect) and not ke._bien_mat:
                if self.co_kiem or self.so_man>=3:
                    msg="Chuot trai de diet"
                    mau=(255,120,120)
                else:
                    msg="Can nhatkiem truoc!"
                    mau=(255,200,60)
                t=self.fn.render(msg,True,mau)
                kx=ke.rect.centerx-cam.lech_x-t.get_width()//2
                ky=ke.rect.top-cam.lech_y-22
                bg=pygame.Surface((t.get_width()+8,t.get_height()+4),pygame.SRCALPHA)
                pygame.draw.rect(bg,(0,0,0,140),(0,0,*bg.get_size()),border_radius=4)
                self.man_hinh.blit(bg,(kx-4,ky-2)); self.man_hinh.blit(t,(kx,ky))

        # Leo hint
        if not self.video.hien:
            nv=self.nhan_vat
            if nv.dang_leo: hint="Dang leo..."
            elif nv.co_the_leo_phai and nv.co_the_leo_trai: hint="Giu chuot+D/A de leo"
            elif nv.co_the_leo_phai: hint="Giu chuot+D de leo"
            elif nv.co_the_leo_trai: hint="Giu chuot+A de leo"
            else: hint=None
            if hint:
                t=self.fn.render(hint,True,(255,230,80))
                nx=nv.rect.centerx-cam.lech_x; ny=nv.rect.top-cam.lech_y-26
                bg=pygame.Surface((t.get_width()+10,t.get_height()+6),pygame.SRCALPHA)
                pygame.draw.rect(bg,(0,0,0,150),(0,0,*bg.get_size()),border_radius=4)
                self.man_hinh.blit(bg,(nx-bg.get_width()//2,ny-2))
                self.man_hinh.blit(t,(nx-t.get_width()//2,ny))

        # Hội thoại vật phẩm
        if self._thoai_vatpham:
            self._ve_thoai_vatpham(w,h)

        # Vẽ quả cầu
        for c in self._ds_cau:
            self.man_hinh.blit(c.image,cam.ap_dung(c))
        # Vẽ kiếm bay (boss10)
        if self.so_man==10:
            for k in self._ds_kiem_bay:
                self.man_hinh.blit(k.image, cam.ap_dung(k))
            for k in self._ds_kiem_mua:
                self.man_hinh.blit(k.image, cam.ap_dung(k))
        # Vẽ kiếm ném (mọi màn)
        for kn in self._ds_kiem_nem:
            self.man_hinh.blit(kn.image, cam.ap_dung(kn))
        # Vẽ boss
        for b in self.ds_boss:
            self.man_hinh.blit(b.image, cam.ap_dung(b))
        # Thanh boss
        if self.so_man==5:
            for b in self.ds_boss:
                con_lai = max(0, (60*FPS - self._boss_timer)/FPS)
                b.ve_thanh_thoi_gian(self.man_hinh,cam.lech_x,cam.lech_y,con_lai,self.fn)
            # Hint chém boss10 (không có ở boss5)
        elif self.so_man==10:
            for b in self.ds_boss:
                b.ve_thanh_mau(self.man_hinh,cam.lech_x,cam.lech_y,self.fn)
            # Label phase
            ph  = getattr(self,'_b10_phase',1)
            lbl = "PHASE 2 — BOSS DIEN" if ph==2 else "PHASE 1"
            mau = (255,80,50) if ph==2 else VANG
            tp  = self.fn.render(lbl, True, mau)
            self.man_hinh.blit(tp, tp.get_rect(center=(w//2, 46)))
            # Đếm ngược 120s
            con_lai=max(0,(120*FPS-self._boss_timer)/FPS)
            t=self.fn.render(f"Con lai: {int(con_lai)}s",True,
                             (220,80,80) if con_lai<20 else VANG)
            self.man_hinh.blit(t,t.get_rect(center=(w//2,28)))
        # Cảnh báo khối rơi
        for kr in self.ds_roi:
            kr.ve_canh_bao(self.man_hinh,cam.lech_x,cam.lech_y,self.fn)
        # Vẽ sao trên map
        for s in self.ds_sao_map:
            self.man_hinh.blit(s.image,cam.ap_dung(s))
        self._ve_nut(w)
        if not self._dang_la_tinh_linh:
            self.tinh_linh.ve(self.man_hinh,cam.lech_x,cam.lech_y,w,h)
        self.video.ve(self.man_hinh)
        self.hud.ve(self.man_hinh, self.nhan_vat, self)

        # ── HUD kiếm ném (F) — giữa dưới ─────────────────
        if self.nhan_vat.so_kiem > 0 or self.so_man == 10:
            if not hasattr(self,'_fn_kiem'):
                self._fn_kiem = pygame.font.SysFont(FONT_CHINH,13,bold=True)
            SZ=44; PAD=10
                        # Đặt bên phải skill dash (offset 54px)
            bx = PAD + 54; by = h - SZ - PAD
            pygame.draw.rect(self.man_hinh,(20,20,45),(bx,by,SZ,SZ),border_radius=8)
            # Icon kiếm nhỏ
            pygame.draw.rect(self.man_hinh,(255,215,0),(bx+8,by+SZ//2-3,SZ-16,6),border_radius=2)
            pygame.draw.polygon(self.man_hinh,(220,235,255),
                [(bx+SZ-10,by+SZ//2-5),(bx+SZ-10,by+SZ//2+5),(bx+SZ-3,by+SZ//2)])
            mau_vien=(255,215,0) if self.nhan_vat.so_kiem>0 else (60,60,80)
            pygame.draw.rect(self.man_hinh,mau_vien,(bx,by,SZ,SZ),2,border_radius=8)
            t=self._fn_kiem.render("F",True,(180,180,200))
            self.man_hinh.blit(t,(bx+SZ-t.get_width()-3,by+2))
            tc=self._fn_kiem.render(str(self.nhan_vat.so_kiem),True,
                                     VANG if self.nhan_vat.so_kiem>0 else (80,80,100))
            self.man_hinh.blit(tc,tc.get_rect(center=(bx+SZ//2,by+SZ-10)))
            if self.so_man == 5 and hasattr(self,'_boss_timer'):
                con_lai = max(0,(60*FPS - self._boss_timer)/FPS)
                self._ve_timer_giua(con_lai, 60, w)
            elif self.so_man == 10 and hasattr(self,'_boss_timer'):
                con_lai = max(0,(120*FPS - self._boss_timer)/FPS)
                self._ve_timer_giua(con_lai, 120, w)
        # Boss5/10 — cảnh báo skill2 đang active
        if self.so_man in (5,10) and getattr(self,'_bsk_sk2_active',False):
            import math as _m
            sec = max(0, self._bsk_sk2_timer // FPS)
            a   = int(200+55*abs(_m.sin(self._bsk_sk2_timer*0.1)))
            fn  = pygame.font.SysFont(FONT_CHINH,18,bold=True)
            t   = fn.render(f"⚠ Khối biến mất! ({sec}s)",True,(255,80,80))
            t.set_alpha(a)
            self.man_hinh.blit(t,t.get_rect(center=(w//2,h-38)))
        self.ket_qua.ve(self.man_hinh)
        if self.tam_dung: self._ve_pause(w,h)

    NUT_S=36; NUT_P=8
    def _ve_nut(self,w):
        s=self.NUT_S; p=self.NUT_P
        self.r_pause=pygame.Rect(w-s-p,p,s,s)
        self.r_mute=pygame.Rect(w-2*s-2*p,p,s,s)
        for r in[self.r_pause,self.r_mute]:
            pygame.draw.rect(self.man_hinh,(30,30,30),r,border_radius=8)
            pygame.draw.rect(self.man_hinh,(180,180,180),r,2,border_radius=8)
        cx,cy=self.r_pause.center
        pygame.draw.rect(self.man_hinh,TRANG,(cx-9,cy-10,7,20))
        pygame.draw.rect(self.man_hinh,TRANG,(cx+2,cy-10,7,20))
        cx2,cy2=self.r_mute.center
        if self.am_bat:
            pygame.draw.polygon(self.man_hinh,TRANG,[(cx2-10,cy2-5),(cx2-2,cy2-5),(cx2+8,cy2-12),(cx2+8,cy2+12),(cx2-2,cy2+5),(cx2-10,cy2+5)])
            pygame.draw.arc(self.man_hinh,TRANG,(cx2+4,cy2-10,12,20),-0.8,0.8,2)
        else:
            pygame.draw.polygon(self.man_hinh,XAM,[(cx2-10,cy2-5),(cx2-2,cy2-5),(cx2+8,cy2-12),(cx2+8,cy2+12),(cx2-2,cy2+5),(cx2-10,cy2+5)])
            pygame.draw.line(self.man_hinh,DO,(cx2+2,cy2-10),(cx2+14,cy2+10),3)

    MUC_P=[("Tiep tuc","tc"),("Choi lai","cl"),("Ve menu","vm")]
    # _ve_thang đã thay bằng ManKetQua
    def _ve_timer_giua(self, con_lai, tong, w):
        """Vẽ đồng hồ đếm ngược giữa trên màn hình."""
        if not hasattr(self,'_fn_timer'):
            self._fn_timer = pygame.font.SysFont(FONT_CHINH, 22, bold=True)
        mau = (220,80,80) if con_lai < tong*0.2 else VANG
        t = self._fn_timer.render(f"{int(con_lai)}s", True, mau)
        # Nền nhỏ
        BW = t.get_width()+20; BH = t.get_height()+8
        bx = w//2 - BW//2; by = 8
        ov = pygame.Surface((BW,BH), pygame.SRCALPHA)
        ov.fill((0,0,0,120))
        pygame.draw.rect(ov, mau, (0,0,BW,BH), 2, border_radius=6)
        self.man_hinh.blit(ov,(bx,by))
        self.man_hinh.blit(t, t.get_rect(center=(w//2, by+BH//2)))



    def _ve_pause(self,w,h):
        ov=pygame.Surface((w,h),pygame.SRCALPHA); ov.fill((0,0,0,160)); self.man_hinh.blit(ov,(0,0))
        ti=self.ft.render("Tam Dung",True,VANG)
        self.man_hinh.blit(ti,ti.get_rect(center=(w//2,h//2-100)))
        self.r_mp=[]
        nw=min(320,w-80); nr=max(40,h//14)
        for i,(nhan,_) in enumerate(self.MUC_P):
            y=h//2-30+i*(nr+10); r=pygame.Rect(w//2-nw//2,y,nw,nr)
            self.r_mp.append(r)
            pygame.draw.rect(self.man_hinh,VANG if i==self.muc_pause else(40,40,80),r,border_radius=10)
            pygame.draw.rect(self.man_hinh,CAM  if i==self.muc_pause else(70,70,130),r,2,border_radius=10)
            chu=self.fm.render(nhan,True,(25,25,25) if i==self.muc_pause else TRANG)
            self.man_hinh.blit(chu,chu.get_rect(center=r.center))

    def xu_ly_su_kien(self,ev):
        if self.video.hien: self.video.xu_ly(ev); return TRANG_THAI_CHOI

        # Click vào nút kết quả thắng/thua
        if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1 and self.ket_qua.hien:
            w2,h2=self.man_hinh.get_size()
            ket=self.ket_qua.xu_ly_click(ev.pos, w2, h2)
            if ket=='choi_lai':
                self.ket_qua.an(); self.tai_man(self.so_man)
            elif ket=='man_tiep':
                self.ket_qua.an(); self.tai_man(min(10,self.so_man+1))
            elif ket=='man_chinh':
                self.ket_qua.an(); return TRANG_THAI_MENU
            return TRANG_THAI_CHOI

        # E — chém boss10 khi đứng gần
                # Boss10: chỉ mất máu khi player ĐANG DASH và chạm rect boss
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_e:
            pass  # E chỉ dùng dash — xử lý hoàn toàn trong xu_ly_phim

                # Nếu không chém được → để xu_ly_phim xử lý dash
        # Q — giáp bất tử (boss 5/10) hoặc hoán đổi (màn khác)
        if ev.type==pygame.KEYDOWN and ev.key==pygame.K_q and not self.tam_dung:
            if self.so_man in (5,10):
                # Màn boss: Q = giáp bất tử 1s, CD 10s
                if self._giap_cd <= 0 and not self._giap_active:
                    self._giap_active = True
                    self._giap_timer  = self.GIAP_TGIAN
                    self._giap_cd     = self.GIAP_CD
            elif self.co_hoan_doi and self.tinh_linh.hien:
                if not self._dang_la_tinh_linh:
                    self._dang_la_tinh_linh = True
                    self._tl_dieu_khien = TinhLinhDieuKhien(
                        self.tinh_linh.x, self.tinh_linh.y)
                else:
                    self._dang_la_tinh_linh = False
                    if self._tl_dieu_khien:
                        self.tinh_linh.x = self._tl_dieu_khien.x
                        self.tinh_linh.y = self._tl_dieu_khien.y
                    self._tl_dieu_khien = None

        # F — đóng thoại vật phẩm hoặc nhặt
        if ev.type==pygame.KEYDOWN and ev.key==pygame.K_f and not self.tam_dung:
            if self._thoai_vatpham:
                self._thoai_vatpham = False   # đóng thoại
            else:
                for k in list(self.ds_kiem):
                    if k.gan_nguoi_choi(self.nhan_vat.rect) and not k._bien_mat:
                        k.bat_dau_bien_mat(); self.co_kiem=True
                        self._thoai_vatpham=True
                for s in list(self.ds_sach):
                    if s.gan_nguoi_choi(self.nhan_vat.rect) and not s._bien_mat:
                        s.bat_dau_bien_mat()
                        self.da_co_dash = True
                        self.nhan_vat.co_dash = True
                        self._thoai_vatpham=True

        # Chuột trái
        if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
            if not self.tam_dung:
                # Click vào nút Y/N cổng
                for dc in self.ds_dc:
                    ket_qua = dc.xu_ly_click_hoi_thoai(ev.pos)
                    if ket_qua == 'co':
                        dest = dc.tra_loi_co(self.nhan_vat.rect)
                        self._teleport(dest[0], dest[1])
                    elif ket_qua == 'khong':
                        dc.tra_loi_khong()
                # Diệt kẻ: cần kiếm (map 1-2) hoặc tự do (map 3+)
                co_the_diet = self.co_kiem or self.so_man >= 3
                if co_the_diet:
                    for ke in list(self.ds_ke):
                        if ke.gan_nguoi_choi(self.nhan_vat.rect) and not ke._bien_mat:
                            ke.bat_dau_bien_mat()
                # Double-click tinh linh
                if self.tinh_linh.hien:
                    wx=ev.pos[0]+self.camera.lech_x
                    wy=ev.pos[1]+self.camera.lech_y
                    self.tinh_linh.xu_ly_click(wx,wy)
            # Nút pause/mute
            if hasattr(self,"r_pause") and self.r_pause.collidepoint(ev.pos):
                self.tam_dung=not self.tam_dung; self.muc_pause=0; return TRANG_THAI_CHOI
            if hasattr(self,"r_mute") and self.r_mute.collidepoint(ev.pos):
                self.am_bat=not self.am_bat; return TRANG_THAI_CHOI
            if self.tam_dung and hasattr(self,"r_mp"):
                for i,r in enumerate(self.r_mp):
                    if r.collidepoint(ev.pos): self.muc_pause=i; return self._do_pause()

        if ev.type==pygame.KEYDOWN:
            if self.tam_dung:
                if ev.key==pygame.K_UP:   self.muc_pause=(self.muc_pause-1)%3
                if ev.key==pygame.K_DOWN: self.muc_pause=(self.muc_pause+1)%3
                if ev.key in(pygame.K_RETURN,pygame.K_ESCAPE): return self._do_pause()
                return TRANG_THAI_CHOI
            if ev.key==pygame.K_ESCAPE: self.tam_dung=True; self.muc_pause=0
            if ev.key==pygame.K_r: self.tai_man(self.so_man)

        if ev.type==pygame.MOUSEMOTION and self.tam_dung:
            if hasattr(self,"r_mp"):
                for i,r in enumerate(self.r_mp):
                    if r.collidepoint(ev.pos): self.muc_pause=i
        return TRANG_THAI_CHOI

    def _do_pause(self):
        a=self.MUC_P[self.muc_pause][1]
        if a=="tc": self.tam_dung=False
        elif a=="cl": self.tai_man(self.so_man)
        elif a=="vm": self.tam_dung=False; return TRANG_THAI_MENU
        return TRANG_THAI_CHOI
