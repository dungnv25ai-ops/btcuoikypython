# cai_dat.py
SCREEN_W = 900; SCREEN_H = 550; FPS = 60
TEN_GAME  = "LOST IN TIME - Quá Khử Lãng Quên"
TILE_SIZE = 48

# Vật lý — nhảy đúng 2 tile (96px)
TRONG_LUC    = 0.8
LUC_NHAY     = -12    # h ≈ 96px = 2 tile
TOC_DO_CHAY  = 5      # chạy nhanh hơn
TOC_DO_TREO  = 3      # leo sách

# Màu
TRANG=(255,255,255); DEN=(0,0,0); XANH_TROI=(100,180,255)
XANH_LA=(60,180,60); DO=(220,60,60); VANG=(255,220,0)
XAM=(120,120,120);   NAU=(139,90,43); CAM=(255,140,0)
FONT_CHINH = "segoeui"

# States
TRANG_THAI_MENU="menu"; TRANG_THAI_CHON_MAN="chon_man"
TRANG_THAI_CHOI="choi"; TRANG_THAI_TRO_CHOI_KHAC="tro_choi_khac"
TRANG_THAI_THONG_TIN="thong_tin"; TRANG_THAI_HUONG_DAN="huong_dan"
TRANG_THAI_THANG="thang"; TRANG_THAI_THUA="thua"
