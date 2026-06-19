                                
def _build(m_str, R, C):
    m = [[' ' for _ in range(C)] for _ in range(R)]
    for r, row_str in enumerate(m_str):
        for c, char in enumerate(row_str):
            if r < R and c < C:
                m[r][c] = char
    return [''.join(row) for row in m]

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

def lay_map_pve(n):

    bang = {
        1: MAP_PE_1,
        2: MAP_PE_2,
    }
    return bang.get(n, None)