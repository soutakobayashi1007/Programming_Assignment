from bingo.balls import BingoBalls


def test_draw_unique_and_range_and_exhaust():
    b = BingoBalls(seed=42)
    seen = set()
    for _ in range(75):
        n = b.draw()
        assert n is not None
        assert 1 <= n <= 75
        assert n not in seen
        seen.add(n)
    # 76回目は尽きる
    assert b.draw() is None
