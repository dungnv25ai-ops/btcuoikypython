# ============================================================
#  man_hinh/thoai_cac_man.py — Nội dung hội thoại từng màn
#
#  Loại 1 — HoiThoai (hộp đen, khi bắt đầu màn):
#    THOAI_MAN[so_man] = [(ten, noi_dung), ...]
#    ten = "" nếu không có tên nhân vật
#
#  Loại 2 — ThongBao (nổi giữa, khi nhặt vật):
#    THONG_BAO_VAT[ten_vat] = (tieu_de, noi_dung)
# ============================================================

# ── Loại 1: Hội thoại đầu màn ────────────────────────────
THOAI_MAN = {

    1: [
        ("", "Nhập nội dung thoại màn 1 dòng 1 vào đây."),
        ("", "Nhập nội dung thoại màn 1 dòng 2 vào đây."),
    ],

    2: [
        ("", "Nhập nội dung thoại màn 2 dòng 1 vào đây."),
    ],

    3: [
        ("", "Nhập nội dung thoại màn 3 dòng 1 vào đây."),
        ("Tinh Linh", "Nhập nội dung thoại màn 3 dòng 2 vào đây."),
    ],

    4: [
        ("", "Nhập nội dung thoại màn 4 dòng 1 vào đây."),
    ],

    5: [
        ("", "Nhập nội dung thoại màn 5 (boss) vào đây."),
    ],

    6: [
        ("", "Nhập nội dung thoại màn 6 vào đây."),
    ],

    7: [
        ("", "Nhập nội dung thoại màn 7 vào đây."),
    ],

    8: [
        ("", "Nhập nội dung thoại màn 8 vào đây."),
    ],

    9: [
        ("", "Nhập nội dung thoại màn 9 vào đây."),
    ],

    10: [
        ("", "Nhập nội dung thoại màn 10 (boss cuối) vào đây."),
    ],

}

# ── Loại 2: Thông báo khi nhặt vật phẩm ─────────────────
THONG_BAO_VAT = {

    # Khi nhặt Kiếm
    "kiem": (
        "Nhặt được Kiếm!",
        "Nhập nội dung thông báo khi nhặt kiếm vào đây.",
    ),

    # Khi nhặt Sách (mở khoá Dash)
    "sach": (
        "Nhặt được Sách!",
        "Nhập nội dung thông báo khi nhặt sách vào đây.",
    ),

    # Khi nhặt Sao
    "sao": (
        "Nhặt được Sao!",
        "Nhập nội dung thông báo khi nhặt sao vào đây.",
    ),

    # Khi nhặt Kiếm rơi từ boss (skill F)
    "kiem_boss": (
        "Nhặt được Kiếm Boss!",
        "Nhập nội dung thông báo khi nhặt kiếm boss vào đây.",
    ),

}
