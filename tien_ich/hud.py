# tien_ich/hud.py — HUD: trái tim + ngôi sao
import pygame
import math, math
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
    SO_TIM = 5
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
        PAD = 10

        # ── Trái tim góc TRÊN TRÁI ───────────────────────
        for i in range(self.SO_TIM):
            img = tt_day if i < self.tim else tt_trong
            y_off = 0
            if self.tim == 1 and i == 0:
                y_off = int(2 * math.sin(self._dem_nhip * 0.2))
            screen.blit(img, (PAD + i*(IW+4), PAD + y_off))

        # ── Ngôi sao góc DƯỚI PHẢI ───────────────────────
        tong_w = self.SO_SAO*(SW+4) - 4
        sx0    = w - tong_w - PAD
        for i in range(self.SO_SAO):
            img = sao_day if i < self.sao else sao_trong
            screen.blit(img, (sx0 + i*(SW+4), h - SW - PAD))

        # ── Skill góc DƯỚI TRÁI ──────────────────────────
        if nhan_vat and nhan_vat.co_dash:
            if dang_tl:
                self._ve_dung_yen(screen, w, h)
            else:
                self._ve_ky_nang_dash(screen, nhan_vat, w, h)
        if man_choi and man_choi.so_man in (5,10):
            self._ve_ky_nang_giap(screen, man_choi, w, h)
        elif man_choi and man_choi.co_hoan_doi:
            self._ve_ky_nang_hoan_doi(screen, nhan_vat, man_choi, w, h)
        # Icon F — kiếm đánh (slot 2, khi co_danh hoặc có so_kiem)
        if nhan_vat and (nhan_vat.co_danh or nhan_vat.so_kiem > 0):
            self._ve_ky_nang_f(screen, nhan_vat, w, h)
        # Icon bay (slot 4, khi co_bay)
        if nhan_vat and nhan_vat.co_bay:
            self._ve_ky_nang_bay(screen, nhan_vat, w, h)


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
        SZ = 44; PAD = 10
        # Slot 3: sau Dash(slot1=PAD) và Kiếm F(slot2=PAD+54)
        bx = PAD + (SZ + 10) * 2
        by = h - SZ - PAD
        dang_doi = mc._dang_la_tinh_linh

        pygame.draw.rect(screen, (20,20,50), (bx,by,SZ,SZ), border_radius=8)
        cx, cy = bx+SZ//2, by+SZ//2
        if dang_doi:
            pygame.draw.circle(screen,(80,200,255),(cx,cy),12,3)
            pygame.draw.polygon(screen,(80,200,255),[(cx-4,cy-16),(cx+4,cy-16),(cx,cy-10)])
            pygame.draw.polygon(screen,(80,200,255),[(cx-4,cy+16),(cx+4,cy+16),(cx,cy+10)])
        else:
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
        """Icon 'Đứng yên' — slot 1, thay thế E khi điều khiển tinh linh."""
        if not hasattr(self, '_font_dung_yen'):
            self._font_dung_yen = pygame.font.SysFont(FONT_CHINH, 13, bold=True)
        SZ = 44; PAD = 10
        bx = PAD; by = h - SZ - PAD

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

    def _ve_ky_nang_bay(self, screen, nv, w, h):
        """Icon bay — slot 4 dưới trái."""
        if not hasattr(self,'_font_bay'):
            self._font_bay = pygame.font.SysFont(FONT_CHINH,13,bold=True)
        SZ=44; PAD=10
        # Slot 4: PAD + (SZ+10)*3
        bx = PAD + (SZ+10)*3; by = h-SZ-PAD
        active = nv._bay_active
        cd     = nv._bay_cd
        timer  = nv._bay_timer

        mau_nen = (10,20,50) if active else (20,20,45)
        pygame.draw.rect(screen, mau_nen, (bx,by,SZ,SZ), border_radius=8)
        # Icon cánh/mũi tên lên
        cx,cy = bx+SZ//2, by+SZ//2
        mau_icon = (100,220,255) if active else (80,80,140) if cd>0 else (140,200,255)
        pygame.draw.polygon(screen, mau_icon, [
            (cx,by+6),(cx-12,cy+4),(cx-5,cy+4),(cx-5,by+SZ-6),(cx+5,by+SZ-6),(cx+5,cy+4),(cx+12,cy+4)])
        # Cooldown overlay
        if cd > 0 and not active:
            tl = cd / nv.BAY_CD
            ov = pygame.Surface((SZ,SZ),pygame.SRCALPHA)
            ov.fill((0,0,0,150)); screen.blit(ov,(bx,by))
            t=self._font_bay.render(f"{cd//60+1}s",True,TRANG)
            screen.blit(t,t.get_rect(center=(bx+SZ//2,by+SZ//2)))
        # Timer đếm ngược khi active
        if active:
            t=self._font_bay.render(f"{timer//60+1}s",True,(100,220,255))
            screen.blit(t,t.get_rect(center=(bx+SZ//2,by+SZ-10)))
        vien = (100,220,255) if active else (60,60,100)
        pygame.draw.rect(screen, vien, (bx,by,SZ,SZ), 2, border_radius=8)
        t=self._font_bay.render("×2",True,(160,180,220))
        screen.blit(t,(bx+SZ-t.get_width()-3,by+2))

    def _ve_ky_nang_f(self, screen, nv, w, h):
        """Icon F đánh thường — slot 2 góc dưới trái."""
        if not hasattr(self,'_font_f'):
            self._font_f = pygame.font.SysFont(FONT_CHINH,13,bold=True)
        SZ=44; PAD=10
        bx = PAD + SZ + 10; by = h-SZ-PAD
        # Nền
        cd = nv._danh_cd
        pygame.draw.rect(screen,(20,20,45),(bx,by,SZ,SZ),border_radius=8)
        # Icon kiếm đơn giản
        cx,cy=bx+SZ//2,by+SZ//2
        pygame.draw.rect(screen,(220,200,30),(bx+10,cy-3,SZ-14,6),border_radius=2)
        pygame.draw.polygon(screen,(220,235,255),
            [(bx+SZ-10,cy-5),(bx+SZ-10,cy+5),(bx+SZ-3,cy)])
        # Overlay cooldown
        if cd > 0:
            pix=int(SZ*cd/nv.DANH_CD)
            ov=pygame.Surface((SZ,pix),pygame.SRCALPHA)
            ov.fill((0,0,0,160))
            screen.blit(ov,(bx,by+SZ-pix))
        mau_vien=(255,215,0) if cd==0 else (80,80,100)
        pygame.draw.rect(screen,mau_vien,(bx,by,SZ,SZ),2,border_radius=8)
        t=self._font_f.render("F",True,(180,180,200))
        screen.blit(t,(bx+SZ-t.get_width()-3,by+2))

    def _ve_ky_nang_giap(self, screen, mc, w, h):
        """Icon giáp bất tử — slot 3 góc dưới trái."""
        if not hasattr(self,'_font_giap'):
            self._font_giap = pygame.font.SysFont(FONT_CHINH,13,bold=True)
        SZ=44; PAD=10
        # Slot 3: bx = PAD + (SZ+10)*2
        bx = PAD + (SZ+10)*2; by = h-SZ-PAD

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
