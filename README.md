#  LOST IN TIME - Quá Khử Lãng Quên

Game 2D puzzle kiểu Mario làm bằng Python + Pygame.

## Cài đặt & Chạy

```bash
# 1. Cài Pygame 
pip install pygame

# 2. Chạy game
cd my_game
python main.py
```

## Điều khiển

| Phím | Hành động |
|------|-----------|
| ← → hoặc A D | Di chuyển |
| Space / W / ↑ | Nhảy |
| R | Chơi lại  |
| F11 | Full màn hình |
| D/→ + Space / W / ↑| Leo lên phải |
| A/← + Space / W / ↑| Leo lên trái |

## Cấu trúc file

```
my_game/
├── main.py                  # Điểm khởi chạy game chính
├── cai_dat.py               # Hằng số, cấu hình hệ thống (Màu sắc, kích thước màn hình, FPS)
├── README.md                # Tài liệu hướng dẫn và giới thiệu dự án
├── man_hinh/                # Quản lý các màn hình và trạng thái của game
│   ├── menu.py              # Màn hình Menu chính khi vào game
│   ├── chon_man.py          # Màn hình lựa chọn màn chơi (Level Selection)
│   ├── huong_dan.py         # Màn hình hiển thị hướng dẫn cách chơi
│   ├── thong_tin.py         # Màn hình thông tin (Credits / Giới thiệu nhóm phát triển)
│   ├── man_choi.py          # Vòng lặp màn chơi chính (Gameplay chính)
│   ├── ban_do.py            # Xử lý nạp, dựng cấu trúc bản đồ từ dữ liệu
│   ├── mapMC.py             # Dữ liệu / Cấu trúc map MC
│   ├── mapPE.py             # Dữ liệu / Cấu trúc map PE
│   ├── boss5_logic.py       # Xử lý logic kịch bản xuất hiện và hành vi riêng của Boss 5
│   ├── boss10_logic.py      # Xử lý logic kịch bản xuất hiện và hành vi riêng của Boss 10
│   ├── thoai_cac_man.py     # Quản lý các đoạn hội thoại, cốt truyện giữa các màn chơi
│   └── tro_choi_khac.py     # Các tính năng mở rộng hoặc chế độ mini-game phụ kèm theo
├── the_gioi/                # Quản lý các thực thể và môi trường hoạt động trong thế giới game
│   ├── nhan_vat.py          # Định nghĩa lớp nhân vật người chơi chính (Player)
│   ├── nen_tang.py          # Định nghĩa khối nền tảng tĩnh (Tile đất, khối tàng hình, cỏ)
│   ├── boss.py              # Định nghĩa lớp cơ sở (Base Class) chung cho các loại Boss
│   ├── hieu_ung.py          # Xử lý các hiệu ứng hình ảnh (Animations, hiệu ứng hạt rơi, nổ)
│   ├── tinh_linh.py         # Thực thể tinh linh đi theo hỗ trợ (Pet / Companion)
│   ├── tinh_linh_dieu_khien.py # Bộ xử lý điều khiển và di chuyển của tinh linh trợ thủ
│   └── vat_the/             # Các vật thể động hoặc có tương tác đặc biệt
│       ├── dan.py           # Xử lý đạn bay, tầm bắn và va chạm gây sát thương
│       ├── ke_di_chuyen.py  # Logic hành vi của quái vật di chuyển thông thường (Quái tuần tra)
│       ├── kiem.py          # Định nghĩa và xử lý đòn đánh của vũ khí (Kiếm)
│       └── moi_truong.py    # Các vật thể môi trường tương tác (Khúc gỗ, khối nước, gai bẫy)
├── tien_ich/                # Các công cụ hỗ trợ hệ thống và thành phần giao diện người dùng (UI)
│   ├── camera.py            # Xử lý camera cuộn màn hình mượt mà theo vị trí nhân vật
│   ├── am_thanh.py          # Trình quản lý, kích hoạt và chuyển đổi âm thanh hệ thống
│   ├── hoi_thoai.py         # Hệ thống khung UI hội thoại và hiển thị chữ chạy
│   ├── hud.py               # Hiển thị thanh trạng thái người chơi (Máu, năng lượng, thanh UI)
│   ├── man_ket_qua.py       # Màn hình thông báo kết quả khi Thắng màn hoặc Thua cuộc (Game Over)
│   ├── nut_back.py          # Thành phần UI nút quay lại (Back Button) dùng chung cho các màn hình
│   └── video_intro.py       # Xử lý phát đoạn phim ngắn / video giới thiệu lúc mở game
└── tai_nguyen/              # Thư mục lưu trữ toàn bộ file tài nguyên Media của game
    ├── hinh_anh/            # Chứa các hình ảnh Spritesheet của nhân vật, quái vật, UI nền
    ├── am_thanh/            # Chứa các tệp tin nhạc nền (BGM) và hiệu ứng âm thanh (SFX)
    ├── khoi/                # Chứa hình ảnh cấu trúc cấu tạo của các block / tiles
    └── skill/               # Chứa hình ảnh đồ họa của các kỹ năng, chiêu thức đặc biệt
```

## Ký hiệu bản đồ (trong man_choi.py)

| Ký hiệu | Ý nghĩa |
| --- | --- |
| `#` | Tile đất |
| `T` | Khối tàng hình |
| `C` | Tile cỏ |
| `W` | Khúc gỗ |
| `K` | Kiếm |
| `S` | Sách |
| `~` | Khối nước |
| `5` | Vị trí sinh Boss 5 |
| `1` | Vị trí sinh Boss 10 |
| `E` | Kẻ địch di chuyển (Quái vật) |
| `$` | Sao map (Vật phẩm thu thập) |
| `R` | Gai (Bẫy) |
| `P` | Vị trí sinh nhân vật (Player) |
| `*` | Ô đích (Đứng vào = qua màn) |
## Tính năng sắp thêm

- [ ] Nhiều màn chơi
- [ ] Cập nhập âm thanh thanh và hình ảnh

