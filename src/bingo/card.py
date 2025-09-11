from __future__ import annotations
from dataclasses import dataclass
import random
from typing import Optional, Dict, Tuple, List


@dataclass
class BingoCard:
    """
    5x5 のBINGOカード。
    - grid[r][c]: マスの数字（N列の中央は None = FREE）
    - opened[r][c]: そのマスが開いているか（FREE中心は True）
    - index[n]: 数字 n -> (行, 列) を O(1) で逆引きする辞書（FREEは登録しない）
    """

    grid: List[List[Optional[int]]]  # ← 中央FREEに対応するため Optional[int]
    opened: List[List[bool]]
    index: Dict[int, Tuple[int, int]]

    @staticmethod
    def from_random(seed: Optional[int] = None) -> "BingoCard":
        rng = random.Random(seed)

        # 5x5 の枠（数字未決定のところは None にしておく）
        grid: List[List[Optional[int]]] = [[None] * 5 for _ in range(5)]
        opened = [[False] * 5 for _ in range(5)]
        index: Dict[int, Tuple[int, int]] = {}

        for col in range(5):
            start = 1 + 15 * col  # 1,16,31,46,61

            if col == 2:
                # N 列は FREE があるので 31-45 から「4つだけ」採用
                nums = rng.sample(range(start, start + 15), 4)
                rows = [0, 1, 3, 4]  # 中央(2,2)を空ける
                for row, n in zip(rows, nums):
                    grid[row][col] = n
                    index[n] = (row, col)
                # FREE（数字なし、最初から開いている）
                grid[2][2] = None
                opened[2][2] = True

            else:
                # 他の列は 5つ
                nums = rng.sample(range(start, start + 15), 5)
                for row in range(5):
                    n = nums[row]
                    grid[row][col] = n
                    index[n] = (row, col)

        return BingoCard(grid=grid, opened=opened, index=index)

    def mark(self, number: int) -> bool:
        """数字がカードにあれば開ける。変化があれば True。"""
        pos = self.index.get(number)
        if pos is None:
            return False
        r, c = pos
        if not self.opened[r][c]:
            self.opened[r][c] = True
            return True
        return False

    def render(self) -> str:
        """
        CUI表示。開いたマスは括弧、FREE は 'F' 表示。
        例:  (F )  ( 7)   23  のように幅をそろえる
        """
        header = "  B   I   N   G   O"
        lines = [header]
        for r in range(5):
            cells = []
            for c in range(5):
                n = self.grid[r][c]
                raw = "F " if n is None else f"{n:>2}"  # 2文字に整形
                cell = f"({raw})" if self.opened[r][c] else f" {raw} "
                cells.append(cell)
            lines.append(" ".join(cells))
        return "\n".join(lines)
