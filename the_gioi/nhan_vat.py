# the_gioi/nhan_vat.py
import pygame
import os as _os
from cai_dat import *

W_NV = TILE_SIZE*2
H_NV = TILE_SIZE * 2

_THU_MUC_GD = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))

# ── Cache ảnh di chuyển (30 ảnh, gốc=trái, flip=phải) ───
_CACHE_DC   = []
_CACHE_DC_F = []

def _load_anh_di_chuyen():
    global _CACHE_DC, _CACHE_DC_F
    if _CACHE_DC:
        return _CACHE_DC, _CACHE_DC_F
    thu_muc = _os.path.join(_THU_MUC_GD, 'tai_nguyen', 'hinh_anh', 'nhan_vat', 'di_chuyen')

    new_w = None  # chiều rộng tính theo tỉ lệ ảnh đầu tiên, áp dụng cho cả 30 frame
    for i in range(1, 31):
        path = _os.path.join(thu_muc, f"{i}.png")
        if not _os.path.isfile(path): break
        try:
            img = pygame.image.load(path).convert_alpha()
            if new_w is None:
                ow, oh = img.get_size()
                new_w = max(1, round(H_NV * ow / oh))
            img = pygame.transform.scale(img, (new_w, H_NV))
            _CACHE_DC.append(img)
            _CACHE_DC_F.append(pygame.transform.flip(img, True, False))
        except Exception:
            pass
    return _CACHE_DC, _CACHE_DC_F


# ── Fallback ─────────────────────────────────────────────
def _ve():
    s = pygame.Surface((W_NV, H_NV), pygame.SRCALPHA)
    pygame.draw.rect(s,(45,95,195),(4,10,W_NV-8,H_NV-10),border_radius=5)
    pygame.draw.rect(s,(75,135,235),(4,10,W_NV-8,3))
    pygame.draw.rect(s,(25,55,145),(4,H_NV-13,W_NV-8,3))
    pygame.draw.rect(s,(230,195,150),(8,2,W_NV-16,18),border_radius=4)
    pygame.draw.rect(s,(225,230,242),(8,0,W_NV-16,5),border_radius=3)
    for ex in [14, W_NV-14]:
        pygame.draw.circle(s,(35,55,155),(ex,11),3)
        pygame.draw.circle(s,(255,255,255),(ex+1,10),1)
    pygame.draw.rect(s,(15,15,35),(4,10,W_NV-8,H_NV-10),2,border_radius=5)
    return s

_SP = _ST = None
def _sprites():
    global _SP, _ST
    if _SP is None:
        _SP = _ve(); _ST = pygame.transform.flip(_SP, True, False)
    return _SP, _ST


# ══════════════════════════════════════════════════════════
#  NHÂN VẬT
# ══════════════════════════════════════════════════════════
class NhanVat(pygame.sprite.Sprite):
    W, H = W_NV, H_NV

    DASH_TOC_DO   = 10
    DASH_FRAMES   = 12
    DASH_COOLDOWN = 45

    # Di chuyển + leo: dùng chung 30 ảnh, 30fps → mỗi ảnh 2 frame game
    _DC_SPD = 2
    _DC_N   = 30
    _DC_MID = 14   # index 0-based của ảnh 15

    def __init__(self, x, y):
        super().__init__()
        # Load ảnh ngay — dùng ảnh 1 (đứng yên) làm frame mặc định
        anh_dc, anh_dc_f = _load_anh_di_chuyen()
        if anh_dc:
            self.image = anh_dc_f[0]   # index 0 = ảnh 1, hướng phải (flip)
        else:
            sp, _ = _sprites()
            self.image = sp
        self.rect     = self.image.get_rect(topleft=(x, y))
        self.vel_x    = 0.0
        self.vel_y    = 0.0
        self.tren_san = False
        self.huong    = 1
        self._khoa    = False

        self._leo_huong = 0

        self.co_dash      = False
        self._dash_frames = 0
        self._dash_dir    = 1
        self._dash_cd     = 0

        self.co_the_leo_phai = False
        self.co_the_leo_trai = False

        self.trong_nuoc = False

        self.so_kiem     = 0
        self._nem_signal = False

        self.co_danh      = False
        self._danh_signal = False
        self._danh_cd     = 0
        self.DANH_CD      = 20

        self.co_bay      = False
        self._bay_active = False
        self._bay_timer  = 0
        self._bay_cd     = 0
        self._jump_count = 0
        self._jump_cd    = 0
        self.BAY_TIME    = 3 * FPS
        self.BAY_CD      = 1 * FPS
        self.JUMP_WINDOW = 18

        self._khoa_hieu_ung  = False
        self._khoa_dong_bang = False

        # Animation di chuyển (dùng chung cho cả leo)
        self._dc_idx               = 0     # index ảnh hiện tại (0-based)
        self._dc_dem               = 0     # đếm frame game
        self._dc_lui               = True  # True=30→15, False=15→30
        self._dc_huong             = 1     # hướng hiện tại của animation
        self._dc_doi_huong_pending = False # đang chờ về ảnh 15 để đổi hướng

    def khoa(self, v): self._khoa = v

    @property
    def dang_leo(self): return self._leo_huong != 0

    @property
    def dang_dash(self): return self._dash_frames > 0

    def _co_khoi_canh(self, ds, sang_phai):
        from the_gioi.nen_tang import KhoiTanHinh
        if sang_phai:
            v = pygame.Rect(self.rect.right, self.rect.top+2, 8, H_NV-4)
        else:
            v = pygame.Rect(self.rect.left-8, self.rect.top+2, 8, H_NV-4)
        return any(v.colliderect(n.rect) for n in ds
                   if not isinstance(n, KhoiTanHinh))

    def kiem_tra_co_the_leo(self, ds):
        self.co_the_leo_phai = self._co_khoi_canh(ds, True)
        self.co_the_leo_trai = self._co_khoi_canh(ds, False)

    # ══════════════════════════════════════════════════════
    #  ANIMATION
    # ══════════════════════════════════════════════════════
    def _cap_nhat_anim(self, dang_di, huong_di):
        """
        dang_di  : True nếu đang di chuyển (kể cả leo tường)
        huong_di : 1 (phải) hoặc -1 (trái)
        Logic ping-pong: 30→15→30→15... khi di chuyển/leo
        Đứng yên: lùi dần về ảnh 1
        Đổi hướng: chạy về ảnh 15 trước rồi mới flip
        """
        anh_dc, anh_dc_f = _load_anh_di_chuyen()
        N   = min(self._DC_N, len(anh_dc)) if anh_dc else 0
        MID = self._DC_MID

        if dang_di:
            # Phát hiện đổi hướng
            if huong_di != self._dc_huong and not self._dc_doi_huong_pending:
                self._dc_doi_huong_pending = True

            self._dc_dem += 1
            if self._dc_dem >= self._DC_SPD:
                self._dc_dem = 0
                if self._dc_doi_huong_pending:
                    # Chạy về ảnh 15
                    if self._dc_idx > MID:
                        self._dc_idx -= 1
                    elif self._dc_idx < MID:
                        self._dc_idx += 1
                    if self._dc_idx == MID:
                        self._dc_huong             = huong_di
                        self._dc_doi_huong_pending = False
                        self._dc_lui               = True
                else:
                    # Ping-pong bình thường
                    if self._dc_lui:
                        self._dc_idx -= 1
                        if self._dc_idx <= MID:
                            self._dc_idx = MID
                            self._dc_lui = False
                    else:
                        self._dc_idx += 1
                        if N > 0 and self._dc_idx >= N - 1:
                            self._dc_idx = N - 1
                            self._dc_lui = True
        else:
            # Đứng yên: lùi về ảnh 1
            self._dc_dem += 1
            if self._dc_dem >= self._DC_SPD:
                self._dc_dem = 0
                if self._dc_idx > 0:
                    self._dc_idx -= 1
            self._dc_doi_huong_pending = False

        # Vẽ ảnh
        if N > 0:
            idx = max(0, min(self._dc_idx, N - 1))
            self.image = anh_dc[idx] if self._dc_huong == -1 else anh_dc_f[idx]
        else:
            sp_p, sp_t = _sprites()
            self.image = sp_p if self.huong == 1 else sp_t

    # ══════════════════════════════════════════════════════
    #  XỬ LÝ PHÍM
    # ══════════════════════════════════════════════════════
    def xu_ly_phim(self, ds, chuot_giu):
        if self._khoa:
            self.vel_x = 0; self._leo_huong = 0; return
        if self._khoa_hieu_ung:
            self.vel_x        = 0
            self.vel_y        = 0
            self._leo_huong   = 0
            self._dash_frames = 0
            self._bay_active  = False
            self._danh_signal = False
            self._nem_signal  = False
            return
        if self._khoa_dong_bang:
            self.vel_x        = 0
            self.vel_y        = 0
            self._leo_huong   = 0
            self._dash_frames = 0
            self._bay_active  = False
            self._nem_signal  = False
            p = pygame.key.get_pressed()
            self._danh_signal = False
            if self._danh_cd > 0: self._danh_cd -= 1
            if p[pygame.K_f] and not hasattr(self, '_f_held'):
                if self.co_danh and self._danh_cd <= 0:
                    self._danh_signal = True
                    self._danh_cd     = self.DANH_CD
            if p[pygame.K_f]: self._f_held = True
            else:
                if hasattr(self, '_f_held'): del self._f_held
            return

        p         = pygame.key.get_pressed()
        muon_phai = p[pygame.K_RIGHT] or p[pygame.K_d]
        muon_trai = p[pygame.K_LEFT]  or p[pygame.K_a]

        if self.dang_dash:
            if muon_phai: self.huong = 1
            if muon_trai: self.huong = -1
            return

        if self.trong_nuoc:
            self._leo_huong = 0
            self.vel_x = 0
            if muon_trai: self.vel_x = -int(TOC_DO_CHAY * 0.55); self.huong = -1
            if muon_phai: self.vel_x =  int(TOC_DO_CHAY * 0.55); self.huong =  1
            if p[pygame.K_SPACE] or p[pygame.K_UP] or p[pygame.K_w]:
                self.vel_y = -4
            return

        if self._bay_cd > 0: self._bay_cd -= 1
        if self._jump_cd > 0: self._jump_cd -= 1

        if self._bay_active:
            self._bay_timer -= 1
            if self._bay_timer <= 0:
                self._bay_active = False
                self._bay_cd     = self.BAY_CD
            self.vel_y = 0; self.vel_x = 0; self._leo_huong = 0
            if muon_trai: self.vel_x = -TOC_DO_CHAY; self.huong = -1
            if muon_phai: self.vel_x =  TOC_DO_CHAY; self.huong =  1
            if self.co_dash and self._dash_cd <= 0 and p[pygame.K_e]:
                self._dash_dir    = self.huong
                self._dash_frames = self.DASH_FRAMES
                self._dash_cd     = self.DASH_COOLDOWN
                self.vel_y        = 0
            return

        muon_leo = p[pygame.K_w] or p[pygame.K_SPACE]
        if muon_leo and (muon_phai or muon_trai):
            sang_phai = muon_phai
            self.huong = 1 if sang_phai else -1
            if self._co_khoi_canh(ds, sang_phai):
                self.vel_x      = 0
                self.vel_y      = -self.TOC_LEO
                self._leo_huong = 1 if sang_phai else -1
                return
            else:
                self._leo_huong = 0
        else:
            self._leo_huong = 0

        self.vel_x = 0
        if muon_trai: self.vel_x = -TOC_DO_CHAY; self.huong = -1
        if muon_phai: self.vel_x =  TOC_DO_CHAY; self.huong =  1

        nhay_phim = p[pygame.K_SPACE] or p[pygame.K_UP] or p[pygame.K_w]
        if nhay_phim and self.tren_san:
            self.vel_y = LUC_NHAY; self.tren_san = False
            self._jump_count = 1; self._jump_cd = self.JUMP_WINDOW
        elif nhay_phim and not self.tren_san and not hasattr(self, '_nhay_held'):
            if self.co_bay and self._bay_cd <= 0 \
                    and self._jump_count >= 1 and self._jump_cd > 0:
                self._bay_active = True; self._bay_timer = self.BAY_TIME
                self._jump_count = 0; self.vel_y = 0
        if nhay_phim: self._nhay_held = True
        else:
            if hasattr(self, '_nhay_held'): del self._nhay_held

        if self.co_dash and self._dash_cd <= 0 and p[pygame.K_e]:
            self._dash_dir    = self.huong
            self._dash_frames = self.DASH_FRAMES
            self._dash_cd     = self.DASH_COOLDOWN
            self.vel_y        = 0

        self._danh_signal = False; self._nem_signal = False
        if self._danh_cd > 0: self._danh_cd -= 1
        if p[pygame.K_f] and not hasattr(self, '_f_held'):
            if self.co_danh and self._danh_cd <= 0:
                self._danh_signal = True; self._danh_cd = self.DANH_CD
        if p[pygame.K_f]: self._f_held = True
        else:
            if hasattr(self, '_f_held'): del self._f_held

        chuot_phai = pygame.mouse.get_pressed()[2]
        if chuot_phai and not hasattr(self, '_r_held'):
            if self.so_kiem > 0:
                self._nem_signal = True; self.so_kiem -= 1
        if chuot_phai: self._r_held = True
        else:
            if hasattr(self, '_r_held'): del self._r_held

    TOC_LEO = 4

    def ap_trong_luc(self):
        if self.dang_leo:    return
        if self.dang_dash:   return
        if self._bay_active: return
        if self.trong_nuoc:
            self.vel_y = min(self.vel_y + TRONG_LUC * 0.3, 3)
        else:
            self.vel_y = min(self.vel_y + TRONG_LUC, 18)

    def di_chuyen(self, ds):
        if self.dang_dash:
            vx = self.DASH_TOC_DO * self._dash_dir
            self._dash_frames -= 1
        else:
            vx = self.vel_x

        buoc   = max(1, abs(int(vx)))
        huong_x = 1 if vx > 0 else (-1 if vx < 0 else 0)
        for _ in range(buoc):
            self.rect.x += huong_x
            for n in ds:
                if self.rect.colliderect(n.rect):
                    if huong_x > 0: self.rect.right = n.rect.left
                    elif huong_x < 0: self.rect.left = n.rect.right
                    if self.dang_dash: self._dash_frames = 0
                    vx = 0; huong_x = 0; break
            if huong_x == 0: break

        self.rect.y += int(self.vel_y)
        self.tren_san = False
        for n in ds:
            if not self.rect.colliderect(n.rect): continue
            if self.vel_y > 0:
                self.rect.bottom = n.rect.top; self.tren_san = True
            elif self.vel_y < 0:
                self.rect.top = n.rect.bottom
            self.vel_y = 0

    def update(self, ds, chuot_trai_giu=False):
        if self._dash_cd > 0: self._dash_cd -= 1
        self.xu_ly_phim(ds, chuot_trai_giu)
        self.ap_trong_luc()
        self.di_chuyen(ds)

        # Leo tường cũng tính là "đang di chuyển" cho animation
        dang_di = ((self.vel_x != 0 or self.dang_leo)
                   and not self.dang_dash
                   and not self._khoa_hieu_ung
                   and not self._khoa_dong_bang)
        self._cap_nhat_anim(dang_di, self.huong)