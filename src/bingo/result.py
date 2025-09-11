from __future__ import annotations
from typing import List, Tuple

GridBool = List[List[bool]]

def _lines(n: int = 5) -> List[List[Tuple[int, int]]]:
    """
    5x5 ビンゴ盤の評価対象ライン（5行 + 5列 + 2斜め = 12本）の
    各セル座標を返す。
    """
    lines: List[List[Tuple[int, int]]] = []
    # 行
    for r in range(n):
        lines.append([(r, c) for c in range(n)])
    # 列
    for c in range(n):
        lines.append([(r, c) for r in range(n)])
    # 斜め2本
    lines.append([(i, i) for i in range(n)])
    lines.append([(i, n - 1 - i) for i in range(n)])
    return lines

# 固定レイアウトなので一度だけ計算して再利用
_LINES = _lines(5)

def count_bingo(opened: GridBool) -> int:
    """完全に開いている（5/5 True）のライン数を数える。"""
    return sum(1 for line in _LINES if all(opened[r][c] for r, c in line))

def count_reach(opened: GridBool) -> int:
    """
    ちょうど 4/5 だけ開いているライン数を数える。
    （ビンゴ済みラインはここには含まれない）
    """
    return sum(
        1
        for line in _LINES
        if sum(1 for r, c in line if opened[r][c]) == 4
    )
