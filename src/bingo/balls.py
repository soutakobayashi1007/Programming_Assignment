import random
from typing import Optional, List


class BingoBalls:
    """1..75 を重複なく1つずつ取り出す抽選機。seedで再現性あり。"""

    def __init__(self, seed: Optional[int] = None) -> None:
        rng = random.Random(seed)
        self._balls: List[int] = list(range(1, 76))
        rng.shuffle(self._balls)
        self._i = 0

    def draw(self) -> Optional[int]:
        if self._i >= len(self._balls):
            return None
        n = self._balls[self._i]
        self._i += 1
        return n

    def remaining(self) -> int:
        return len(self._balls) - self._i
