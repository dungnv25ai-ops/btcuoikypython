import pygame
from cai_dat import *
from tien_ich.nut_back import ve_nut_back as _ve_nut_back, ve_nen_chung

# Giữ nguyên Thể loại chung 1 dòng sạch sẽ như bạn muốn
NOI_DUNG = [
    ("Tên trò chơi",  TEN_GAME),
    ("Thể loại",      "2D-platformer, phiêu lưu, hành động, giải đố, nhập vai"),
    ("Công cụ",       "Python 3 + Pygame"),
    ("Số màn chơi",   "10 màn  (Boss ở màn 5 và màn 10)"),
    ("Phiên bản",     "v1.0 (demo)"),
    ("Lập trình",     "Nguyễn Văn Dũng - 25AI008"),
]

class ThongTin:
    def __init__(self, man_hinh):
        self.man_hinh = man_hinh
        self._r_back  = None
        self._tao_font()

    def _tao_font(self):
        w, h = self.man_hinh.get_size()
        self.font_tieude  = pygame.font.SysFont(FONT_CHINH, max(24, h//14), bold=True)
        self.font_nhan    = pygame.font.SysFont(FONT_CHINH, max(14, h//26), bold=True)
        self.font_gia_tri = pygame.font.SysFont(FONT_CHINH, max(14, h//26))
        self.font_nho     = pygame.font.SysFont(FONT_CHINH, max(13, h//38))

    def update(self):
        self._tao_font()

    def ve(self):
        w, h = self.man_hinh.get_size()
        ve_nen_chung(self.man_hinh)

        self._r_back = _ve_nut_back(self.man_hinh, self.font_nho)

        tieu = self.font_tieude.render("Thông tin trò chơi", True, VANG)
        ty = h // 10
        self.man_hinh.blit(tieu, tieu.get_rect(center=(w//2, ty)))

        so_dong   = len(NOI_DUNG)
        vung_cao  = h * 0.68
        dong_cao  = vung_cao / so_dong
        bat_dau_y = h * 0.22
        le_x      = w * 0.1
        
        # 1. Thụt lề cột chữ giá trị vào một chút (từ 0.45 giảm còn 0.4) để có nhiều khoảng trống hơn
        cot2_x    = w * 0.4 
        
        # 2. Tính toán bề rộng tối đa mà chữ được phép hiển thị bên trong ô hình chữ nhật
        r_phai_toan_bo = le_x - 8 + w * 0.8
        max_w_chu      = int(r_phai_toan_bo - cot2_x - 15) 

        for i, (nhan, gia_tri) in enumerate(NOI_DUNG):
            y   = int(bat_dau_y + i * dong_cao)
            r   = pygame.Rect(int(le_x-8), y-4, int(w*0.8), int(dong_cao-6))
            mau = (30,30,65) if i%2==0 else (22,22,50)
            pygame.draw.rect(self.man_hinh, mau, r, border_radius=8)
            
            # Vẽ Nhãn (Ví dụ: "Thể loại") - luôn căn giữa ô theo chiều dọc
            t_n = self.font_nhan.render(nhan, True, CAM)
            cy_n = r.centery - t_n.get_height() // 2
            self.man_hinh.blit(t_n, (int(le_x), cy_n))
            
            # 3. THUẬT TOÁN TỰ ĐỘNG XUỐNG DÒNG (Word-Wrap)
            words = gia_tri.split(' ')
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                # Nếu dòng thử nghiệm vẫn vừa với kích thước ô thì cộng dồn vào
                if self.font_gia_tri.size(test_line)[0] <= max_w_chu:
                    current_line = test_line
                else:
                    # Ngược lại, đẩy dòng hiện tại vào danh sách và ngắt sang dòng mới
                    if current_line: lines.append(current_line)
                    current_line = word
            if current_line: lines.append(current_line)
            
            # 4. Tính toán vị trí Y để toàn bộ các dòng chữ giá trị được căn giữa hoàn hảo trong ô
            h_chu = self.font_gia_tri.get_height()
            khoang_cach_dong = 2
            tong_cao_chu = len(lines) * h_chu + (len(lines) - 1) * khoang_cach_dong
            bat_dau_y_chu = r.centery - tong_cao_chu // 2
            
            # Tiến hành vẽ từng dòng chữ giá trị
            for idx, line in enumerate(lines):
                t_g = self.font_gia_tri.render(line, True, TRANG)
                line_y = bat_dau_y_chu + idx * (h_chu + khoang_cach_dong)
                self.man_hinh.blit(t_g, (int(cot2_x), int(line_y)))

    def xu_ly_su_kien(self, su_kien):
        if su_kien.type == pygame.KEYDOWN and su_kien.key == pygame.K_ESCAPE:
            return TRANG_THAI_MENU
        if su_kien.type == pygame.MOUSEBUTTONDOWN and su_kien.button == 1:
            if self._r_back and self._r_back.collidepoint(su_kien.pos):
                return TRANG_THAI_MENU
        return TRANG_THAI_THONG_TIN