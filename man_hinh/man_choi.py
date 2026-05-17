# man_hinh/man_choi.py
import pygame
from cai_dat import *
from the_gioi.nhan_vat  import NhanVat
from the_gioi.nen_tang  import NenTang, NenTangBoss, KhucGo, ODict
from the_gioi.tinh_linh import TinhLinh
from the_gioi.tinh_linh_dieu_khien import TinhLinhDieuKhien
from the_gioi.vat_the   import Kiem, KeDiChuyen, Sach1x1, KhoiDichChuyen, KhoiRoi, QuaCau
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
    fill(8,11,0,80)
    m[6][1]='P'; m[6][10]='K'
    fill(8,11,22,26)=""; m[7][28]='E'
    fill(1,2,25,28); fill(1,2,35,38);fill(1,2,45,48); fill(1,2,55,58);fill(1,2,65,68); fill(1,2,75,78)
    m[0][26]='E'; m[0][36]='E'; m[0][46]='E'; m[0][56]='E'; m[0][66]='E'; m[0][76]='E'
    m[0][77]='*'
    m[0][25]='$'; m[0][35]='$'
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
    R,C=11,80
    m=[[' ']*C for _ in range(R)]
    def fill(r1,r2,c1,c2,ch='#'):
        for r in range(r1,r2):
            for c in range(c1,c2):
                if 0<=r<R and 0<=c<C: m[r][c]=ch
    fill(8,11,0,80)
    m[6][1]='P'; m[6][8]='$'
    fill(0,7,20,21); fill(0,7,22,23)
    m[5][28]='$'
    fill(0,5,40,41); fill(3,8,44,45); fill(0,5,48,49)
    m[3][52]='$'
    fill(3,8,60,80)
    m[2][77]='*'
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
    7:  [(6,10),(4,30),(5,48)],
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
    fill(8,12,0,5); fill(8,12,10,15); fill(8,12,20,25)
    fill(8,12,30,35); fill(8,12,40,45)
    m[6][1]='P'
    m[2][97]='*'
    fill(3,12,50,70)
    m[2][55]='*'; m[1][55]='*'; m[0][55]='*'
    return [''.join(r) for r in m]

MAP_7 = _gen_map7()

def _gen_map_boss5():
    R,C=11,40
    m=[[' ']*C for _ in range(R)]
    def fill(r1,r2,c1,c2,ch='#'):
        for r in range(r1,r2):
            for c in range(c1,c2):
                if 0<=r<R and 0<=c<C: m[r][c]=ch
    fill(0,1,0,40); fill(9,11,0,40)
    fill(0,11,0,1); fill(0,11,39,40)
    fill(6,7,6,12); fill(6,7,18,24); fill(6,7,28,34)
    m[6][2]='P'
    m[5][3]='$'; m[5][20]='$'; m[5][36]='$'
    return [''.join(r) for r in m]

def _gen_map_boss10():
    R,C=11,40
    m=[[' ']*C for _ in range(R)]
    def fill(r1,r2,c1,c2,ch='#'):
        for r in range(r1,r2):
            for c in range(c1,c2):
                if 0<=r<R and 0<=c<C: m[r][c]=ch
    fill(0,1,0,40); fill(9,11,0,40)
    fill(0,11,0,1); fill(0,11,39,40)
    fill(4,5,5,12); fill(4,5,20,28); fill(4,5,30,37)
    fill(7,8,8,16); fill(7,8,24,32)
    m[6][2]='P'
    m[3][6]='$'; m[3][25]='$'; m[3][32]='$'
    return [''.join(r) for r in m]

MAP_BOSS_5  = _gen_map_boss5()
MAP_BOSS_10 = _gen_map_boss10()

def _lay_map(n):
    if   n==1:  return MAP_1,False
    elif n==2:  return MAP_2,False
    elif n==3:  return MAP_3,False
    elif n==4:  return MAP_4,False
    elif n==5:  return MAP_BOSS_5,True
    elif n==6:  return MAP_6,False
    elif n==7:  return MAP_7,False
    elif n==10: return MAP_BOSS_10,True
    return MAP_4,False

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
        self._ds_cau=None   # group quả cầu boss
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
        self.co_hoan_doi = (n >= 4)
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
                # Cổng A: khu2→khu3
                elif o=='A' and ri==6 and ci==25: self.ds_dc.add(KhoiDichChuyen(ci,ri,41,6))
                # Cổng C: khu3→khu2 (chiều ngược A)
                elif o=='C' and ri==6 and ci==41: self.ds_dc.add(KhoiDichChuyen(ci,ri,35,6))
                # Cổng B: khu3→khu4
                elif o=='B' and ri==6 and ci==71: self.ds_dc.add(KhoiDichChuyen(ci,ri,82,1))
                # Cổng D: khu4→khu3 (chiều ngược B)
                elif o=='D' and ri==1 and ci==82: self.ds_dc.add(KhoiDichChuyen(ci,ri,71,6))
                elif o=='E': self.ds_ke.add(KeDiChuyen(ci,ri,20,40))
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
        self.spawn_pos=(sx*T,sy*T)
        # Spawn boss
        if self.so_man==5:
            self.ds_boss.add(Boss5(19,7))   # giữa arena, đứng trên sàn
        elif self.so_man==10:
            self.ds_boss.add(Boss10(19,7))
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
        else:
            # Màn 5-10: tinh linh luôn có mặt
            self.tinh_linh.bat_dau(sx*T+T*2,sy*T)

    def _hoi_sinh(self):
        self.nhan_vat.rect.topleft=self.spawn_pos
        self.nhan_vat.vel_y=self.nhan_vat.vel_x=0

    def _teleport(self, dest_x, dest_y):
        self.nhan_vat.rect.topleft=(dest_x, dest_y)
        self.nhan_vat.vel_y=0; self.nhan_vat.vel_x=0

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
            self._tl_dieu_khien.update()

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
        self.nhan_vat.update(tat_ca, chuot_trai_giu=chuot_giu)
        self.tinh_linh.update(self.nhan_vat.rect)
        if self._dang_la_tinh_linh and self._tl_dieu_khien:
            self.camera.cap_nhat_vi_tri(
                self._tl_dieu_khien.rect.centerx,
                self._tl_dieu_khien.rect.centery)
        else:
            self.camera.cap_nhat(self.nhan_vat)
        self.ds_kiem.update()
        self.ds_ke.update(self.ds_nen)
        # Quái tấn công người chơi
        if self._i_frames <= 0:
            for ke in list(self.ds_ke):
                hit, dx, dy = ke.kiem_tra_tan_cong(self.nhan_vat.rect, self._i_frames)
                if hit:
                    if 1 <= self.so_man <= 4:
                        # Màn 1-4: chỉ đẩy lùi, không mất mạng
                        self.nhan_vat.vel_y = -9    # Giữ nguyên độ nảy cao như ý bạn
                        self._i_frames = KeDiChuyen.I_FRAMES
                        
                        # SỬA Ở ĐÂY: Giảm từ 15 xuống 8 frame
                        self.so_frame_day = 8   
                        self.huong_day_lui = dx  
                    elif 6 <= self.so_man <= 9:
                        # Màn 6-9: mất mạng
                        go = self.hud.mat_mang()
                        if go: self.ket_qua.hien_thua(self.so_man)
                        else:
                            self.nhan_vat.vel_y = -9
                            self._i_frames = KeDiChuyen.I_FRAMES
                            
                            # SỬA Ở ĐÂY: Giảm từ 15 xuống 8 frame
                            self.so_frame_day = 8   
                            self.huong_day_lui = dx  
                    # Màn 5, 10: quái hiền, không làm gì
                    break
        
        # ==============================================================
        # Xử lý ép đẩy lùi vật lý
        if hasattr(self, 'so_frame_day') and self.so_frame_day > 0:
            self.so_frame_day -= 1
            # SỬA Ở ĐÂY: Chỉ lùi 1 pixel mỗi frame
            # Tổng cộng lùi: 8 frame * 1 pixel = 8 pixel 
            self.nhan_vat.rect.x += self.huong_day_lui * 1

        if self._i_frames > 0: self._i_frames -= 1
        # Boss bắn cầu
        self._ds_cau.update()
        if self.so_man in (5,10):
            for b in self.ds_boss:
                if hasattr(b,'_ban_cd') and b._ban_cd <= 0 and not b._tu_luc:
                    b.chuan_bi_ban(self.nhan_vat.rect.centerx,
                                   self.nhan_vat.rect.centery)
                if hasattr(b,'can_ban') and b.can_ban:
                    b.can_ban = False
                    self._ds_cau.add(QuaCau(
                        b.rect.centerx, b.rect.centery,
                        b._ban_sx, b._ban_sy))
                    b._ban_cd = b.BAN_COOLDOWN
            # Cầu chạm player
            for c in list(self._ds_cau):
                if c.cham_nguoi(self.nhan_vat.rect) and not self._giap_active:
                    c.kill()
                    go = self.hud.mat_mang()
                    if go: self.ket_qua.hien_thua(self.so_man)
                    else:  self._hoi_sinh()
        self.ds_sach.update()
        self.ds_dc.update()
        # Cổng dịch chuyển — xử lý hội thoại
        for dc in self.ds_dc:
            dc.xu_ly_vung(self.nhan_vat.rect)
        self.ds_boss.update()
        self.ds_sao_map.update()
        # Boss logic
        if self.so_man == 5 and self.ds_boss:
            self._boss_timer += 1
            # Chạm boss → mất mạng (trừ khi đang có giáp)
            for b in self.ds_boss:
                if b.cham_nguoi(self.nhan_vat.rect) and not self._giap_active:
                    go = self.hud.mat_mang()
                    if go: self.ket_qua.hien_thua(self.so_man)
                    else:  self._hoi_sinh()
                    break
            # Sống sót 60 giây → thắng
            if self._boss_timer >= 60*FPS and not self.ket_qua.hien:
                self._boss_win = True
                self.da_thang  = True
                self.ket_qua.hien_thang(self.so_man, self.hud.sao)
        elif self.so_man == 10:
            self._boss_timer += 1
            for b in list(self.ds_boss):
                # Chạm boss → mất mạng
                if b.cham_nguoi(self.nhan_vat.rect) and not self._giap_active:
                    go = self.hud.mat_mang()
                    if go: self.ket_qua.hien_thua(self.so_man)
                    else:  self._hoi_sinh()
                    break
            # Hết 60s mà boss chưa chết → thua
            if self._boss_timer >= 60*FPS and self.ds_boss and not self.ket_qua.hien:
                self.ket_qua.hien_thua(self.so_man)
            # Boss chết → thắng
            if not self.ds_boss and not self.ket_qua.hien:
                self._boss_win = True
                self.da_thang  = True
                self.ket_qua.hien_thang(self.so_man, self.hud.sao)
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
        if self.nhan_vat.rect.top>len(self.ban_do)*T+50:
            game_over=self.hud.mat_mang()
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
            # Đếm ngược 60s
            con_lai=max(0,(60*FPS-self._boss_timer)/FPS)
            t=self.fn.render(f"Con lai: {int(con_lai)}s",True,
                             (220,80,80) if con_lai<15 else VANG)
            self.man_hinh.blit(t,t.get_rect(center=(w//2,28)))
        # Cảnh báo khối rơi
        for kr in self.ds_roi:
            kr.ve_canh_bao(self.man_hinh,cam.lech_x,cam.lech_y,self.fn)
        # Vẽ sao trên map
        for s in self.ds_sao_map:
            self.man_hinh.blit(s.image,cam.ap_dung(s))
        t=self.fn.render(f"Man {self.so_man}",True,TRANG)
        tb=self.fn.render(f"Man {self.so_man}",True,DEN)
        self.man_hinh.blit(tb,(13,13)); self.man_hinh.blit(t,(12,12))
        self._ve_nut(w)
        if not self._dang_la_tinh_linh:
            self.tinh_linh.ve(self.man_hinh,cam.lech_x,cam.lech_y,w,h)
        self.video.ve(self.man_hinh)
        self.hud.ve(self.man_hinh, self.nhan_vat, self)
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
        if ev.type==pygame.KEYDOWN and ev.key==pygame.K_e:
            if self.so_man==10 and not self.nhan_vat.co_dash:
                # Nếu không có dash, E dùng để chém boss
                for b in list(self.ds_boss):
                    if b.rect.inflate(T,T).colliderect(self.nhan_vat.rect):
                        chet = b.nhan_don()
                        break
            elif self.so_man==10 and self.nhan_vat.co_dash:
                # Có dash: kiểm tra xem E là dash hay chém boss
                # Nếu gần boss → chém boss, nếu không → dash
                chem=False
                for b in list(self.ds_boss):
                    if b.rect.inflate(T*2,T*2).colliderect(self.nhan_vat.rect):
                        b.nhan_don(); chem=True; break
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
