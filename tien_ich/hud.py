# tien_ich/hud.py — HUD: trái tim + ngôi sao
import pygame, math
from cai_dat import *

def _ve_trai_tim(r=14, day=False):
    S = r*2+4
    s = pygame.Surface((S,S), pygame.SRCALPHA)
    mau = (220,50,60) if day else (60,20,25)
    vien= (255,100,110) if day else (100,40,50)
    # Vẽ trái tim bằng 2 hình tròn + tam giác
    pygame.draw.circle(s, mau, (r//2+2, r//2+1), r//2)
    pygame.draw.circle(s, mau, (r+r//2+2, r//2+1), r//2)
    pygame.draw.polygon(s, mau, [(2, r//2+2),(S-2, r//2+2),(S//2, S-2)])
    if day:
        pygame.draw.circle(s, vien, (r//2+3, r//2), r//2-2)
    return s

def _ve_sao(r=13, day=False):
    S = r*2+4
    s = pygame.Surface((S,S), pygame.SRCALPHA)
    mau = (255,210,0) if day else (60,55,20)
    vien= (255,240,120) if day else (100,90,30)
    cx,cy = S//2, S//2
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i*36)
        ri  = r if i%2==0 else r//2
        pts.append((cx + ri*math.cos(ang), cy + ri*math.sin(ang)))
    pygame.draw.polygon(s, mau, pts)
    if day:
        pygame.draw.polygon(s, vien, pts, 2)
    return s

# Cache
_TT_DAY = _TT_TRONG = _SAO_DAY = _SAO_TRONG = None
def _get_sprites():
    global _TT_DAY,_TT_TRONG,_SAO_DAY,_SAO_TRONG
    if _TT_DAY is None:
        _TT_DAY   = _ve_trai_tim(14, True)
        _TT_TRONG = _ve_trai_tim(14, False)
        _SAO_DAY  = _ve_sao(13, True)
        _SAO_TRONG= _ve_sao(13, False)
    return _TT_DAY,_TT_TRONG,_SAO_DAY,_SAO_TRONG


class HUD:
    SO_TIM = 3
    SO_SAO = 3

    def __init__(self):
        self.tim  = self.SO_TIM
        self.sao  = 0
        self._dem_nhip = 0

    def reset(self):
        self.tim = self.SO_TIM
        self.sao = 0

    def mat_mang(self):
        self.tim = max(0, self.tim - 1)
        return self.tim <= 0   # True = game over

    def nhat_sao(self):
        self.sao = min(self.SO_SAO, self.sao + 1)

    def ve(self, screen, nhan_vat=None, man_choi=None):
        dang_tl = bool(man_choi and man_choi._dang_la_tinh_linh)
        w, h = screen.get_size()
        tt_day,tt_trong,sao_day,sao_trong = _get_sprites()
        self._dem_nhip += 1

        IW = tt_day.get_width()
        SW = sao_day.get_width()
        PAD = 8

        # ── Trái tim bên TRÁI ────────────────────────────
        for i in range(self.SO_TIM):
            img = tt_day if i < self.tim else tt_trong
            y_off = 0
            if self.tim == 1 and i == 0:
                y_off = int(2 * math.sin(self._dem_nhip * 0.2))
            screen.blit(img, (PAD + i*(IW+4), PAD + y_off))

        # ── Ngôi sao GIỮA ────────────────────────────────
        tong_w = self.SO_SAO*(SW+4) - 4
        sx0    = (w - tong_w)//2
        for i in range(self.SO_SAO):
            img = sao_day if i < self.sao else sao_trong
            screen.blit(img, (sx0 + i*(SW+4), PAD))

        # ── Kỹ năng Dash góc dưới trái ───────────────────
        if nhan_vat and nhan_vat.co_dash:
            if dang_tl:
                self._ve_dung_yen(screen, w, h)   # nhân vật đứng yên
            else:
                self._ve_ky_nang_dash(screen, nhan_vat, w, h)
        if man_choi and man_choi.so_man in (5,10):
            self._ve_ky_nang_giap(screen, man_choi, w, h)
        elif man_choi and man_choi.co_hoan_doi:
            self._ve_ky_nang_hoan_doi(screen, nhan_vat, man_choi, w, h)


    def _ve_ky_nang_dash(self, screen, nv, w, h):
        if not hasattr(self, '_font_ky_nang'):
            self._font_ky_nang = pygame.font.SysFont(FONT_CHINH, 13, bold=True)

        DASH_CD_MAX = nv.DASH_COOLDOWN
        cd_con_lai  = nv._dash_cd
        sang_cd     = cd_con_lai / DASH_CD_MAX

        SZ  = 44
        PAD = 10
        bx  = PAD                     # ← BÊN TRÁI
        by  = h - SZ - PAD

        # Nền ô
        mau_nen = (25,25,45)
        pygame.draw.rect(screen, mau_nen, (bx,by,SZ,SZ), border_radius=8)

        # Icon dash (tia sét)
        cx, cy = bx+SZ//2, by+SZ//2
        pts = [(cx+4,by+5),(cx-2,cy-1),(cx+3,cy-1),(cx-4,by+SZ-5)]
        pygame.draw.lines(screen,(255,215,0),False,pts,3)

        # Overlay hồi chiêu (màu tối che lên icon)
        if sang_cd > 0:
            pix = int(SZ * sang_cd)
            ov  = pygame.Surface((SZ, pix), pygame.SRCALPHA)
            ov.fill((0,0,0,160))
            screen.blit(ov,(bx, by+SZ-pix))
            # Số giây còn lại
            giay = cd_con_lai / 60
            t = self._font_ky_nang.render(f"{giay:.1f}s", True, TRANG)
            screen.blit(t, t.get_rect(center=(bx+SZ//2, by+SZ//2)))

        # Viền: vàng nếu sẵn, xám nếu đang hồi
        mau_vien = (255,215,0) if sang_cd == 0 else (80,80,100)
        pygame.draw.rect(screen, mau_vien, (bx,by,SZ,SZ), 2, border_radius=8)

        # Nhãn phím
        t_phim = self._font_ky_nang.render("E", True, (180,180,200))
        screen.blit(t_phim, (bx+SZ-t_phim.get_width()-3, by+2))

    def _ve_ky_nang_hoan_doi(self, screen, nv, mc, w, h):
        if not hasattr(self, '_font_hoan_doi'):
            self._font_hoan_doi = pygame.font.SysFont(FONT_CHINH, 13, bold=True)
        SZ  = 44; PAD = 10
        # Hoán đổi: luôn bên phải
        bx  = w - SZ - PAD
        by  = h - SZ - PAD
        dang_doi = mc._dang_la_tinh_linh

        mau_nen  = (20,20,50)
        pygame.draw.rect(screen, mau_nen, (bx,by,SZ,SZ), border_radius=8)

        # Icon: 2 mũi tên xoay (hoán đổi)
        cx, cy = bx+SZ//2, by+SZ//2
        if dang_doi:
            # Đang là tinh linh: icon sáng cyan
            pygame.draw.circle(screen,(80,200,255),(cx,cy),12,3)
            pygame.draw.polygon(screen,(80,200,255),[(cx-4,cy-16),(cx+4,cy-16),(cx,cy-10)])
            pygame.draw.polygon(screen,(80,200,255),[(cx-4,cy+16),(cx+4,cy+16),(cx,cy+10)])
        else:
            # Bình thường: icon trắng xanh
            pygame.draw.circle(screen,(140,160,220),(cx,cy),12,2)
            pygame.draw.polygon(screen,(140,160,220),[(cx-4,cy-15),(cx+4,cy-15),(cx,cy-9)])
            pygame.draw.polygon(screen,(140,160,220),[(cx-4,cy+15),(cx+4,cy+15),(cx,cy+9)])

        vien = (80,200,255) if dang_doi else (80,80,120)
        pygame.draw.rect(screen, vien, (bx,by,SZ,SZ), 2, border_radius=8)
        t = self._font_hoan_doi.render("Q", True, (180,200,240))
        screen.blit(t, (bx+SZ-t.get_width()-3, by+2))
        tl = self._font_hoan_doi.render("Tinh linh" if dang_doi else "Nhan vat",
                                         True, (80,200,255) if dang_doi else (140,160,200))
        screen.blit(tl, tl.get_rect(center=(bx+SZ//2, by+SZ+10)))

    def _ve_dung_yen(self, screen, w, h):
        """Icon 'Đứng yên' ở góc dưới trái — hiện khi đang điều khiển tinh linh."""
        if not hasattr(self, '_font_dung_yen'):
            self._font_dung_yen = pygame.font.SysFont(FONT_CHINH, 13, bold=True)
        SZ  = 44; PAD = 10
        bx  = PAD; by = h - SZ - PAD

        # Nền tối
        pygame.draw.rect(screen,(20,20,45),(bx,by,SZ,SZ),border_radius=8)

        # Icon nhân vật đứng yên (ký hiệu dừng/pause)
        cx, cy = bx+SZ//2, by+SZ//2
        # 2 thanh dọc kiểu pause
        pygame.draw.rect(screen,(140,150,180),(cx-10,cy-12,7,24),border_radius=2)
        pygame.draw.rect(screen,(140,150,180),(cx+3, cy-12,7,24),border_radius=2)

        # Viền xám
        pygame.draw.rect(screen,(80,85,110),(bx,by,SZ,SZ),2,border_radius=8)

        # Label
        t = self._font_dung_yen.render("Dung", True, (140,150,180))
        screen.blit(t, t.get_rect(center=(bx+SZ//2, by+SZ+10)))

    def _ve_ky_nang_giap(self, screen, mc, w, h):
        """Icon giáp bất tử ở góc dưới phải — màn boss."""
        import math
        if not hasattr(self,'_font_giap'):
            self._font_giap = pygame.font.SysFont(FONT_CHINH,13,bold=True)
        SZ=44; PAD=10
        bx=w-SZ-PAD; by=h-SZ-PAD

        active = mc._giap_active
        cd     = mc._giap_cd
        cd_max = mc.GIAP_CD

        pygame.draw.rect(screen,(15,15,40),(bx,by,SZ,SZ),border_radius=8)
        # Icon khiên
        cx,cy=bx+SZ//2,by+SZ//2
        mau=(80,200,255) if active else (80,80,130) if cd>0 else (120,220,255)
        pygame.draw.polygon(screen,mau,[
            (cx,by+4),(cx+16,cy-4),(cx+16,cy+8),(cx,by+SZ-4),(cx-16,cy+8),(cx-16,cy-4)])
        pygame.draw.polygon(screen,(200,240,255),[
            (cx,by+4),(cx+16,cy-4),(cx+16,cy+8),(cx,by+SZ-4),(cx-16,cy+8),(cx-16,cy-4)],2)

        # Overlay cooldown
        if cd > 0 and not active:
            tl=cd/cd_max
            ov=pygame.Surface((SZ,SZ),pygame.SRCALPHA)
            ov.fill((0,0,0,150))
            screen.blit(ov,(bx,by))
            t=self._font_giap.render(f"{cd//60}s",True,TRANG)
            screen.blit(t,t.get_rect(center=(bx+SZ//2,by+SZ//2)))

        # Active: glow
        if active:
            r=int(24+4*math.sin(mc._giap_timer*0.3))
            g=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
            pygame.draw.circle(g,(100,220,255,60),(r,r),r)
            screen.blit(g,(bx+SZ//2-r,by+SZ//2-r))
            t=self._font_giap.render(f"{mc._giap_timer//60+1}s",True,(100,220,255))
            screen.blit(t,t.get_rect(center=(bx+SZ//2,by+SZ-10)))

        vien=(80,200,255) if active else (60,60,100)
        pygame.draw.rect(screen,vien,(bx,by,SZ,SZ),2,border_radius=8)
        t=self._font_giap.render("Q",True,(160,180,220))
        screen.blit(t,(bx+SZ-t.get_width()-3,by+2))
        lbl=self._font_giap.render("Giap" if not active else "BAT TU",
                                    True,(80,200,255) if active else (120,130,160))
        screen.blit(lbl,lbl.get_rect(center=(bx+SZ//2,by+SZ+10)))
