import pygame
from cai_dat import *
from tien_ich.nut_back import ve_nut_back as _ve_nut_back, ve_nen_chung

CAC_MUC_HUONG_DAN = [
    ("DI CHUYỂN",  [
        ("← →  hoặc  A D",  "Chạy sang trái / phải"),
        ("Space / W / ↑",   "Nhảy lên"),
    ]),
    ("MỤC TIÊU", [
        ("Ô vàng",       "Đứng vào đây để qua màn"),
    ]),
    ("PHÍM HỆ THỐNG", [
        ("ESC",             "Quay lại menu"),
        ("R",               "Chơi lại màn hiện tại"),
        ("F11",             "Bật / tắt toàn màn hình"),
    ]),
    ("MÀN ĐẶC BIỆT", [
        ("Màn 5",           "Boss Đại Tinh Linh — Chỉ cần câu hết 60 giây là thắng"),
        ("Màn 10",          "Boss DoHiTo — Tiêu diệt boss trong 120 giây để thắng"),
    ]),
    ("CÁC SKILL", [
        ("F",               "Tấn công (mở khóa ở màn 2)"),
        ("E",               "Lướt (mở khóa ở màn 3)"),
        ("Q",           "Hoán đổi (chỉ dùng ở màn 4)"),
        ("Q",           "Bất tử (chỉ dùng ở màn BOSS)"),
    ]),
    ("SKILL BOSS", [
        ("Đại Tinh Linh",           "Có skill trói chân, đóng băng, laze, cầu lửa"),
        ("Đặt biệt",           "Trúng đòn laze trong trạng thái đóng băng sát thương sẽ bỏ qua bất tử"),
        ("DoHiTo",          "Có 2 thanh máu, với nhiều skill gây sát thương nhưng lại ít khống chế"),
        ("Đặt biệt",          "Khi lượng máu từ 5 trở xuống, boss có thể tung skill trói chân và hồi máu cho bản thân"),
    ]),
]

class HuongDan:
    def __init__(self, man_hinh):
        self.man_hinh = man_hinh
        self._r_back  = None
        self._tao_font()

    def _tao_font(self):
        w, h = self.man_hinh.get_size()
        self.font_tieude   = pygame.font.SysFont(FONT_CHINH, max(26, h//14), bold=True)
        self.font_nhom     = pygame.font.SysFont(FONT_CHINH, max(14, h//28), bold=True)
        self.font_noi_dung = pygame.font.SysFont(FONT_CHINH, max(13, h//32))
        self.font_nho      = pygame.font.SysFont(FONT_CHINH, max(12, h//40))

    def update(self):
        pass

    def ve(self):
        w, h = self.man_hinh.get_size()
        ve_nen_chung(self.man_hinh)

        self._r_back = _ve_nut_back(self.man_hinh, self.font_nho)

        tieu = self.font_tieude.render(" Hướng Dẫn Chơi", True, VANG)
        self.man_hinh.blit(tieu, tieu.get_rect(center=(w//2, h//12)))

        cot_x = [w//8, w//2 + 40] 
        y_bat_dau = h//7
        
        h_font_tieude = self.font_nhom.get_height()
        h_font_noidung = self.font_noi_dung.get_height()
        
        # Khe hở tối thiểu giữa các dòng khi bị ngắt dòng
        khe_ho_dong = 2 
        
        khe_ho_khung = max(8, h // 60) 
        
        # Tính toán chiều rộng khung (ví dụ: 35% màn hình)
        width_khung = int(w * 0.35) 
        
        # Tính toán phần không gian dành cho chữ mô tả (trừ đi phần chữ phím và lề)
        # Giả sử chữ phím chiếm tối đa 120px (bạn có thể chỉnh số này)
        toa_do_x_mo_ta_tuong_doi = 130 
        max_w_mo_ta = width_khung - toa_do_x_mo_ta_tuong_doi - 10 # 10px lề phải

        y_hien_tai = [y_bat_dau, y_bat_dau + (h_font_noidung + 12) * 2] 

        for idx, (nhom, ds) in enumerate(CAC_MUC_HUONG_DAN):
            cot = idx % 2 
            y = y_hien_tai[cot]

            t_nhom = self.font_nhom.render(nhom, True, CAM)
            self.man_hinh.blit(t_nhom, (cot_x[cot], y))
            
            y += h_font_tieude + 8 

            for phim, mo_ta in ds:
                t_phim = self.font_noi_dung.render(phim, True, VANG)
                
                # --- THUẬT TOÁN TỰ ĐỘNG XUỐNG DÒNG CHO MÔ TẢ ---
                words = mo_ta.split(' ')
                lines = []
                current_line = ""
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    if self.font_noi_dung.size(test_line)[0] <= max_w_mo_ta:
                        current_line = test_line
                    else:
                        if current_line: lines.append(current_line)
                        current_line = word
                if current_line: lines.append(current_line)
                
                # Tính chiều cao khung dựa trên số dòng của mô tả
                so_dong = max(1, len(lines))
                h_khung = (so_dong * h_font_noidung) + ((so_dong - 1) * khe_ho_dong) + 12 # 12px lề trên/dưới
                
                # Vẽ khung với chiều cao tự động co giãn
                r = pygame.Rect(cot_x[cot] - 10, y, width_khung, h_khung)
                pygame.draw.rect(self.man_hinh, (30,30,65), r, border_radius=6)
                
                # Vẽ phím (căn giữa theo chiều dọc của khung)
                cy_phim = y + (h_khung - h_font_noidung) // 2
                self.man_hinh.blit(t_phim, (cot_x[cot], cy_phim))
                
                # Vẽ từng dòng của phần mô tả
                tong_cao_chu_mo_ta = (so_dong * h_font_noidung) + ((so_dong - 1) * khe_ho_dong)
                bat_dau_y_mo_ta = y + (h_khung - tong_cao_chu_mo_ta) // 2
                
                for i, line in enumerate(lines):
                    t_mo = self.font_noi_dung.render(line, True, (200,200,200))
                    line_y = bat_dau_y_mo_ta + i * (h_font_noidung + khe_ho_dong)
                    self.man_hinh.blit(t_mo, (cot_x[cot] + toa_do_x_mo_ta_tuong_doi, line_y))
                
                y += h_khung + khe_ho_khung 
                
            y += h_font_tieude 
            
            y_hien_tai[cot] = y

    def xu_ly_su_kien(self, su_kien):
        if su_kien.type == pygame.KEYDOWN and su_kien.key == pygame.K_ESCAPE:
            return TRANG_THAI_MENU
        if su_kien.type == pygame.MOUSEBUTTONDOWN and su_kien.button == 1:
            if self._r_back and self._r_back.collidepoint(su_kien.pos):
                return TRANG_THAI_MENU
        return TRANG_THAI_HUONG_DAN