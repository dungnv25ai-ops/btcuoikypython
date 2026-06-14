# tien_ich/nut_back.py — Hàm tiện ích vẽ nút ◀ Quay lại
import pygame
from cai_dat import *

def ve_nut_back(screen, font):
    """Vẽ nút ◀ Quay lại góc trên trái, trả về rect."""
    p = 10; NW = 110; NH = 34
    r = pygame.Rect(p, p, NW, NH)
    mx, my = pygame.mouse.get_pos()
    hv = r.collidepoint(mx, my)
    pygame.draw.rect(screen, (50,50,100) if hv else (30,30,70), r, border_radius=8)
    pygame.draw.rect(screen, (140,140,220) if hv else (80,80,140), r, 2, border_radius=8)
    t = font.render("◀  Quay lại", True,
                    (220,220,255) if hv else (160,160,210))
    screen.blit(t, t.get_rect(center=r.center))
    return r


# ── Nền chung cho các màn trước khi chơi ─────────────────
import os as _os
_CACHE_NEN_CHUNG = {}

def ve_nen_chung(screen):
    """Vẽ ảnh tai_nguyen/hinh_anh/nen.png scale vừa màn hình,
    phủ lớp tối mờ lên trên. Fallback fill tối nếu chưa có ảnh."""
    w, h = screen.get_size()
    key = (w, h)
    if key not in _CACHE_NEN_CHUNG:
        path = _os.path.join(
            _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
            'tai_nguyen', 'hinh_anh', 'nen.png')
        surf = None
        if _os.path.isfile(path):
            try:
                img  = pygame.image.load(path).convert()
                surf = pygame.transform.scale(img, (w, h))
            except Exception:
                pass
        _CACHE_NEN_CHUNG[key] = surf

    nen = _CACHE_NEN_CHUNG[key]
    if nen:
        screen.blit(nen, (0, 0))
        # Lớp tối mờ nhẹ đè lên
        ov = pygame.Surface((w, h), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 120))
        screen.blit(ov, (0, 0))
    else:
        screen.fill((18, 18, 40))
