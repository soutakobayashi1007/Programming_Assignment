from bingo.card import BingoCard


def test_card_column_ranges_uniqueness_and_free_center():
    c = BingoCard.from_random(seed=123)

    for col in range(5):
        start = 1 + 15 * col
        rows = [0, 1, 2, 3, 4]
        if col == 2:  # N列は中央FREEを除外
            rows = [0, 1, 3, 4]

        vals = {c.grid[r][col] for r in rows}
        assert len(vals) == (4 if col == 2 else 5)
        assert all(v is not None for v in vals)
        assert all(start <= v < start + 15 for v in vals)

    # 中央FREEの性質
    assert c.opened[2][2] is True
    assert c.grid[2][2] is None

    # カード全体の数字は 24 個（FREE除く）でユニーク
    nums = [c.grid[r][q] for r in range(5) for q in range(5) if not (r == 2 and q == 2)]
    assert len(set(nums)) == 24


def test_mark_marks_exact_cell_and_returns_bool():
    c = BingoCard.from_random(seed=7)
    n = c.grid[0][0]
    assert n is not None
    assert c.opened[0][0] is False
    ok = c.mark(n)
    assert ok is True and c.opened[0][0] is True

    # 存在しない数字（0など）は False
    before = [row[:] for row in c.opened]
    ok2 = c.mark(0)
    assert ok2 is False and c.opened == before
