# man_hinh/mapPE.py — Bản đồ PvE
# Góc nhìn: zoom out full map (giống màn 5, 10)
# Thêm map: thêm MAP_PE_N rồi đăng ký trong lay_map_pve()

def _build(m_str, R, C):
    m = [[' ' for _ in range(C)] for _ in range(R)]
    for r, row_str in enumerate(m_str):
        for c, char in enumerate(row_str):
            if r < R and c < C:
                m[r][c] = char
    return [''.join(row) for row in m]


# ══════════════════════════════════════════════════════════
#  MAP PvE 1  (dùng tạm MAP_BOSS_5)
# ══════════════════════════════════════════════════════════
MAP_PE_1 = _build([
    "                                        ",
    "                                      $ ",
    "                                      E ",
    "                                      # ",
    "                                      $ ",
    "                                      E ",
    "                                      # ",
    "                                      $ ",
    "                                        ",
    "  P                                     ",
    "########################################",
], 11, 40)


# ══════════════════════════════════════════════════════════
#  MAP PvE 2  (dùng tạm MAP_BOSS_10)
# ══════════════════════════════════════════════════════════
MAP_PE_2 = _build([
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "     P                          ",
    "                                ",
    "################################",
], 11, 32)


# ══════════════════════════════════════════════════════════
#  Hàm lấy map
# ══════════════════════════════════════════════════════════
def lay_map_pve(n):
    """Trả về ban_do hoặc None nếu chưa có."""
    bang = {
        1: MAP_PE_1,
        2: MAP_PE_2,
    }
    return bang.get(n, None)
