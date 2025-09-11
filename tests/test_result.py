from bingo.result import count_reach, count_bingo

def blank_opened(n: int = 5, free_center: bool = False):
    opened = [[False] * n for _ in range(n)]
    if free_center:
        opened[2][2] = True
    return opened

def test_start_state_with_free_has_no_reach_or_bingo():
    o = blank_opened(free_center=True)
    assert count_reach(o) == 0
    assert count_bingo(o) == 0

def test_row_reach_and_bingo():
    o = blank_opened()
    # 行0を4つ開ける（リーチ）
    o[0] = [True, True, True, True, False]
    assert count_reach(o) == 1
    assert count_bingo(o) == 0
    # 行0を5つ開ける（ビンゴ）
    o[0][4] = True
    assert count_reach(o) == 0          # ビンゴはリーチに含めない
    assert count_bingo(o) == 1

def test_col_and_diag_reaches():
    o = blank_opened()
    # 列1をリーチ（上から4つ）
    for r in range(4):
        o[r][1] = True
    # 主対角線をリーチ（左上→右下）
    for i in range(5):
        o[i][i] = True
    o[2][2] = False  # 対角線のどこか1つだけ閉じる
    assert count_reach(o) == 2
    assert count_bingo(o) == 0

def test_multiple_bingos_counted_independently():
    o = blank_opened()
    # 行2をビンゴ
    o[2] = [True] * 5
    # 列4をビンゴ
    for r in range(5):
        o[r][4] = True
    assert count_bingo(o) == 2
    assert count_reach(o) == 0
