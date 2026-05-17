# the_gioi/nhan_vat.py
import pygame
from cai_dat import *

W_NV = TILE_SIZE
H_NV = TILE_SIZE * 2

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


class NhanVat(pygame.sprite.Sprite):
    W, H = W_NV, H_NV

    # Hằng số dash
    DASH_TOC_DO   = 10    # px/frame trong khi dash
    DASH_FRAMES   = 12    # số frame dash
    DASH_COOLDOWN = 45    # frame hồi chiêu

    def __init__(self, x, y):
        super().__init__()
        sp, _ = _sprites()
        self.image    = sp
        self.rect     = self.image.get_rect(topleft=(x, y))
        self.vel_x    = 0.0
        self.vel_y    = 0.0
        self.tren_san = False
        self.huong    = 1
        self._khoa    = False

        # Leo tường
        self._leo_huong = 0

        # Dash
        self.co_dash      = False
        self._dash_frames = 0    # > 0 = đang dash
        self._dash_dir    = 1
        self._dash_cd     = 0

        # Hint UI
        self.co_the_leo_phai = False
        self.co_the_leo_trai = False

    def khoa(self, v): self._khoa = v

    @property
    def dang_leo(self): return self._leo_huong != 0

    @property
    def dang_dash(self): return self._dash_frames > 0

    # ── Kiểm tra khối cạnh bên (dùng cho leo) ─────────────
    def _co_khoi_canh(self, ds, sang_phai):
        if sang_phai:
            v = pygame.Rect(self.rect.right, self.rect.top+2, 8, H_NV-4)
        else:
            v = pygame.Rect(self.rect.left-8, self.rect.top+2, 8, H_NV-4)
        return any(v.colliderect(n.rect) for n in ds)

    def kiem_tra_co_the_leo(self, ds):
        self.co_the_leo_phai = self._co_khoi_canh(ds, True)
        self.co_the_leo_trai = self._co_khoi_canh(ds, False)

    # ── Xử lý phím ────────────────────────────────────────
    def xu_ly_phim(self, ds, chuot_giu):
        if self._khoa:
            self.vel_x = 0; self._leo_huong = 0; return

        p         = pygame.key.get_pressed()
        muon_phai = p[pygame.K_RIGHT] or p[pygame.K_d]
        muon_trai = p[pygame.K_LEFT]  or p[pygame.K_a]

        # ── Đang dash: chỉ cập nhật hướng, không override vel_x ──
        if self.dang_dash:
            if muon_phai: self.huong = 1
            if muon_trai: self.huong = -1
            return

        # ── Leo tường: giữ chuột + D/A ────────────────────
        if chuot_giu and (muon_phai or muon_trai):
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

        # ── Di chuyển bình thường ─────────────────────────
        self.vel_x = 0
        if muon_trai: self.vel_x = -TOC_DO_CHAY; self.huong = -1
        if muon_phai: self.vel_x =  TOC_DO_CHAY; self.huong =  1

        if (p[pygame.K_SPACE] or p[pygame.K_UP] or p[pygame.K_w]) and self.tren_san:
            self.vel_y = LUC_NHAY; self.tren_san = False

        # ── Kích hoạt dash ────────────────────────────────
        if self.co_dash and self._dash_cd <= 0 and p[pygame.K_e]:
            self._dash_dir    = self.huong
            self._dash_frames = self.DASH_FRAMES
            self._dash_cd     = self.DASH_COOLDOWN
            self.vel_y        = 0

    TOC_LEO = 4

    # ── Trọng lực ─────────────────────────────────────────
    def ap_trong_luc(self):
        if self.dang_leo:  return   # leo tường: không rơi
        if self.dang_dash: return   # đang dash: không rơi
        self.vel_y = min(self.vel_y + TRONG_LUC, 18)

    # ── Di chuyển + collision ──────────────────────────────
    def di_chuyen(self, ds):
        # Ngang: dùng vel_x khi bình thường, DASH_TOC_DO khi dash
        if self.dang_dash:
            vx = self.DASH_TOC_DO * self._dash_dir
            self._dash_frames -= 1
        else:
            vx = self.vel_x

        # Di chuyển ngang từng bước nhỏ ← tránh xuyên tường
        buoc = max(1, abs(int(vx)))
        huong_x = 1 if vx > 0 else (-1 if vx < 0 else 0)
        for _ in range(buoc):
            self.rect.x += huong_x
            for n in ds:
                if self.rect.colliderect(n.rect):
                    if huong_x > 0: self.rect.right = n.rect.left
                    elif huong_x < 0: self.rect.left = n.rect.right
                    # Nếu đang dash và chạm tường → dừng dash
                    if self.dang_dash: self._dash_frames = 0
                    vx = 0; huong_x = 0
                    break
            if huong_x == 0: break

        # Di chuyển dọc
        self.rect.y += int(self.vel_y)
        self.tren_san = False
        for n in ds:
            if not self.rect.colliderect(n.rect): continue
            if self.vel_y > 0:
                self.rect.bottom = n.rect.top
                self.tren_san    = True
            elif self.vel_y < 0:
                self.rect.top    = n.rect.bottom
            self.vel_y = 0

    # ── Update chính ──────────────────────────────────────
    def update(self, ds, chuot_trai_giu=False):
        if self._dash_cd > 0: self._dash_cd -= 1
        self.xu_ly_phim(ds, chuot_trai_giu)
        self.ap_trong_luc()
        self.di_chuyen(ds)
        sp_p, sp_t = _sprites()
        self.image = sp_p if self.huong == 1 else sp_t
