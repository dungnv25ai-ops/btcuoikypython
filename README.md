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
| R | Chơi lại (khi thắng) |
| ESC | Về menu |

## Cấu trúc file

```
my_game/
├── main.py                  # Điểm khởi chạy
├── cai_dat.py               # Hằng số, cấu hình
├── the_gioi/
│   ├── nhan_vat.py          # Nhân vật người chơi
│   └── nen_tang.py          # Tile đất, ô đích, hộp gỗ
├── man_hinh/
│   ├── menu.py              # Màn hình menu
│   └── man_choi.py          # Màn chơi chính
├── tien_ich/
│   └── camera.py            # Camera cuộn theo nhân vật
└── tai_nguyen/
    ├── hinh_anh/            # Để ảnh PNG vào đây sau
    └── am_thanh/            # Để file âm thanh vào đây sau
```

## Ký hiệu bản đồ (trong man_choi.py)

| Ký hiệu | Ý nghĩa |
|---------|---------|
| `#` | Tile đất |
| `P` | Vị trí sinh nhân vật |
| `*` | Ô đích (đứng vào = qua màn) |
| `H` | Hộp gỗ có thể đẩy |
| ` ` | Không khí |

## Tính năng sắp thêm

- [ ] Nhiều màn chơi
- [ ] Sprite + animation
- [ ] Âm thanh
- [ ] Kẻ thù
