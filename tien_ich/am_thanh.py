                                                              
import os
import pygame

_THU_MUC = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),             
    "tai_nguyen", "am_thanh"
)

_NHAC_NEN = {
    "menu"       : "nen",
    "man_1_4"    : "nhac",
    "man_6_9"    : "nhac",
    "boss_5"     : "nhac",
    "boss_10_p1" : "nhac",
    "boss_10_p2" : "nhac",
}

_DUOI_UU_TIEN = [".mp3", ".ogg", ".wav"]

def _tim_file(ten_goc):

    for duoi in _DUOI_UU_TIEN:
        path = os.path.join(_THU_MUC, ten_goc + duoi)
        if os.path.isfile(path):
            return path
    return None

class AmThanh:

    def __init__(self, am_luong_nhac=0.7, am_luong_sfx=1.0):
                               
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        self._nhac_hien_tai = None
        self._nhac_path     = None
        self._toc_do_hien   = 1.0
        self._am_luong_nhac = am_luong_nhac
        self._am_luong_sfx  = am_luong_sfx
        self._sfx_click     = self._tai_sfx("click")
        self._tat           = False                           

    def _tai_sfx(self, ten):
        path = _tim_file(ten)
        if path:
            try:
                return pygame.mixer.Sound(path)
            except Exception:
                pass
        return None

    def dat_toc_do(self, toc_do: float):

        try:
                                                           
            freq_goc, size, channels = pygame.mixer.get_init()
            freq_moi = int(freq_goc / toc_do)                          
            if not hasattr(self, '_nhac_path') or not self._nhac_path:
                return
            vi_tri = pygame.mixer.music.get_pos() / 1000.0
            pygame.mixer.quit()
            pygame.mixer.init(frequency=freq_moi, size=size, channels=channels, buffer=512)
            pygame.mixer.music.load(self._nhac_path)
            pygame.mixer.music.set_volume(self._am_luong_nhac)
            pygame.mixer.music.play(-1, start=vi_tri)
            self._toc_do_hien = toc_do
        except Exception:
            pass

    def choi_nhac(self, key: str):

        if self._tat:
            return
        if key == self._nhac_hien_tai:
            return

        ten = _NHAC_NEN.get(key)
        if ten is None:
            return

        path = _tim_file(ten)
        if path is None:
            pygame.mixer.music.stop()
            self._nhac_hien_tai = None
            return

        try:
                                             
            if hasattr(self, '_toc_do_hien') and self._toc_do_hien != 1.0:
                freq_goc = 44100
                pygame.mixer.quit()
                pygame.mixer.init(frequency=freq_goc, size=-16, channels=2, buffer=512)
                self._toc_do_hien = 1.0
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self._am_luong_nhac)
            pygame.mixer.music.play(-1)
            self._nhac_hien_tai = key
            self._nhac_path     = path
        except Exception:
            self._nhac_hien_tai = None

    def phat_click(self):

        if self._tat or self._sfx_click is None:
            return
        try:
            self._sfx_click.set_volume(self._am_luong_sfx)
            self._sfx_click.play()
        except Exception:
            pass

    def dung(self):

        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        self._nhac_hien_tai = None

    def tam_dung(self):

        try:
            pygame.mixer.music.pause()
        except Exception:
            pass

    def tiep_tuc(self):

        if self._tat:
            return
        try:
            pygame.mixer.music.unpause()
        except Exception:
            pass

    def tang_am(self, muc: float):

        self._am_luong_nhac = max(0.0, min(1.0, muc))
        try:
            pygame.mixer.music.set_volume(self._am_luong_nhac)
        except Exception:
            pass

    def tang_am_sfx(self, muc: float):

        self._am_luong_sfx = max(0.0, min(1.0, muc))

    def tat_am(self, tat: bool):

        self._tat = tat
        if tat:
            self.dung()

    @property
    def dang_phat(self):
        return self._nhac_hien_tai