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
        ("Tinh Linh", "Này, tỉnh lại đi, bạn có sao không?"),
        ("NGười chơi", "Đây là đâu? Mà sao tôi lại ở đây?"),
        ("Tinh Linh", "Rơi từ trên trời xuống mà xông mất mạng, đúng là phi thường. Mà bạn còn nhớ mình là ai không vậy?"),
        ("NGười chơi", "Tôi... tôi hình như không nhớ gì cả."),
        ("Tinh Linh", "Mà theo tui thấy không lầm thì bạn bay từ hướng kia tới đây, có lẽ bạn nên tới đó thử biết đâu có người quen"),
        ("Tinh Linh", "Mà nếu bạn không phiền chúng ta có thể cùng nhau đến đó, vì tôi cũng có việc đi đến hướng đó."),
        ("NGười chơi", "Vậy phiền bạn cùng tôi đi đến đó nhé! Mà bạn tên gì nhỉ?"),
        ("SaSaKi(Tinh Linh)", "Tôi là SaSiKi, mà bạn hình như bạn không nhớ tên đúng không, vậy tui sẽ gọi bạn là KiKiSa nhé?"),
        ("KiKiSa(NGười chơi)", "KiKiSa nghe cũng hay đấy! Cảm ơn bạn đã giúp tôi, SaSiKi!"),
    ],

    2: [
        ("SaSaKi(Tinh Linh)", "Nhìn kia phía trước có 1 cây kiếm, mà bạn hình như cũng không có vũ khí nhặt nó lên và sài thử xem."),
        ("KiKiSa(NGười chơi)", "Nhặt kiếm như vậy, liệu có ổn không?."),
        ("SaSaKi(Tinh Linh)", "Mà gần đây cũng chắc có, ai chắc là 1 cây kiếm vô chủ thôi."),
        ("SaSaKi(Tinh Linh)", "Mà cũng cũng hay phía trước cũng có mấy con slime bạn cầm thử kiếm rồi làm vài đường xem có thuận tay không."),
    ],

    3: [
        ("KiKiSa(NGười chơi)", "Nhìn kìa đằng  kia có 1 cuốn sách ở dưới đất"),
        ("SaSaKi(Tinh Linh)", "Ở đâu, à thấy rồi, mắt cũng tinh ghê."),
        ("SaSaKi(Tinh Linh)", "Lại nhặt thử biết đâu là 1 cuốn sách bí kiếp gì đó."),
    ],

    4: [
        ("KiKiSa(NGười chơi)", "Phía trước hình như có 1 ngôi nhà, ngôi nhà này là của ai nhỉ?"),
        ("SaSaKi(Tinh Linh)", "Hm Hm! Xin giới thiệu với bạn ngôi nhà phía trước là của Đại Tinh Linh, người bảo vệ của khu rừng này"),  
        ("SaSaKi(Tinh Linh)", "Để vào nhà xem có gì?"),  
        ("KiKiSa(NGười chơi)", "Vào nhà của người khác, khi họ vắng nhà là không tốt đâu."),
    ],

    5: [
        ("KiKiSa(NGười chơi)", "Tới nơi rồi, cậu hình như bay từ bên kia qua."),
        ("SaSaKi(Tinh Linh)", "Mà hình như bên kia cũng có người thì phải?"),
        ("KiKiSa(NGười chơi)", "Bộ cậu không nhìn ra sao, đó là Đại Tinh Linh mà lúc trước tớ đã nhắt."),
        ("SaSaKi(Tinh Linh)", "Đ"),        
        ("KiKiSa(NGười chơi)", "Tới nơi rồi, cậu hình như bay từ bên kia qua."),
        ("SaSaKi(Tinh Linh)", "Mà hình như bên kia cũng có người thì phải?"),    
    ],

    6: [
        ("KiKiSa(NGười chơi)", "Nhập nội dung thoại màn 6 vào đây."),
    ],

    7: [
        ("KiKiSa(NGười chơi)", "Nhập nội dung thoại màn 7 vào đây."),
        ("SaSaKi(Tinh Linh)", "Nhập nội dung thoại màn 7 dòng 2 vào đây."),
    ],

    8: [
        ("KiKiSa(NGười chơi)", "Nhập nội dung thoại màn 8 vào đây."),
        ("SaSaKi(Tinh Linh)", "Nhập nội dung thoại màn 8 dòng 2 vào đây."), 
    ],

    9: [
        ("KiKiSa(NGười chơi)", "Nhập nội dung thoại màn 9 vào đây."),
        ("SaSaKi(Tinh Linh)", "Nhập nội dung thoại màn 9 dòng 2 vào đây."), 
    ],

    10: [
        ("KiKiSa(NGười chơi)", "Nhập nội dung thoại màn 10 (boss cuối) vào đây."),
        ("SaSaKi(Tinh Linh)", "Nhập nội dung thoại màn 10 dòng 2 vào đây."),
    ],

}

# ── Loại 2: Thông báo khi nhặt vật phẩm ─────────────────
THONG_BAO_VAT = {

    # Khi nhặt Kiếm
    "kiem": (
        "Nhặt được Kiếm!",
        "Bạn có thể nhấn F để tấn công.",
    ),

    # Khi nhặt Sách (mở khoá Dash)
    "sach": (
        "Nhặt được Sách!",
        "Bạn có thể nhấn E để sử dụng kỹ năng lướt tới 1 đoạn ngắn.",
    ),
}
