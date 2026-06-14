# tien_ich/video_intro.py
import os
import pygame
from cai_dat import *


class VideoIntro:
    """Phát video intro từ tai_nguyen/video/intro_001.png..."""
    _THU_MUC = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "tai_nguyen", "video")
    _SPDF = 3   # số frame game mỗi ảnh video

    def __init__(self):
        self.hien    = False
        self._frames = []
        self._idx    = 0
        self._dem    = 0
        self._rs     = None
        self.fn      = None
        self._loaded = False

    def bat(self):
        self.hien = True; self._idx = 0; self._dem = 0; self._loaded = False

    def _load(self, screen):
        if self._loaded: return
        self._loaded = True
        frames = []
        if os.path.isdir(self._THU_MUC):
            w, h = screen.get_size()
            for i in range(1, 10000):
                path = os.path.join(self._THU_MUC, f"intro_{i:03d}.png")
                if not os.path.isfile(path): break
                try:
                    img = pygame.image.load(path).convert()
                    frames.append(pygame.transform.scale(img, (w, h)))
                except Exception:
                    break
        self._frames = frames
        if not self._frames: self.hien = False

    def update(self):
        if not self.hien or not self._frames: return
        self._dem += 1
        if self._dem >= self._SPDF:
            self._dem = 0; self._idx += 1
            if self._idx >= len(self._frames): self.hien = False

    def ve(self, screen):
        if not self.hien: return
        self._load(screen)
        if not self._frames or self._idx >= len(self._frames):
            self.hien = False; return
        w, h = screen.get_size()
        screen.blit(self._frames[self._idx], (0, 0))
        if not self.fn:
            self.fn = pygame.font.SysFont(FONT_CHINH, max(14, h//36))
        SW, SH = 150, 36
        sx = w - SW - 14; sy = h - SH - 14
        self._rs = pygame.Rect(sx, sy, SW, SH)
        mx, my = pygame.mouse.get_pos(); hv = self._rs.collidepoint(mx, my)
        pygame.draw.rect(screen, (60,60,80) if hv else (25,25,40), self._rs, border_radius=7)
        pygame.draw.rect(screen, (120,120,180), self._rs, 1, border_radius=7)
        ts = self.fn.render("Bỏ qua  ▶▶", True, (210,210,230))
        screen.blit(ts, ts.get_rect(center=self._rs.center))

    def xu_ly(self, ev):
        if not self.hien: return False
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self._rs and self._rs.collidepoint(ev.pos):
                self.hien = False; return True
        if ev.type == pygame.KEYDOWN and ev.key in (
                pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
            self.hien = False; return True
        return False
