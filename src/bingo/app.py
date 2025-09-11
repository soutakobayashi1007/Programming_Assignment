from __future__ import annotations
from typing import Optional, Dict, Any
from .balls import BingoBalls
from .card import BingoCard
from .result import count_reach, count_bingo

class Session:
    """
    CLI/GUI 共通の極小ゲーム管理。
    - 起動直後は未開始（card/balls とも None）
    - new_game() で開始、draw_once() で1球進める
    - status() は表示に必要な最小情報を dict で返す（complete=ビンゴ12）
    """
    def __init__(self) -> None:
        self.balls: Optional[BingoBalls] = None
        self.card:  Optional[BingoCard]  = None
        self.last:  Optional[int]        = None

    # --- ライフサイクル ---
    def new_game(self, seed: Optional[int] = None) -> None:
        self.balls = BingoBalls(seed=seed)
        self.card  = BingoCard.from_random(seed=seed)
        self.last  = None

    def reset_blank(self) -> None:
        self.balls = None
        self.card  = None
        self.last  = None

    def started(self) -> bool:
        return self.balls is not None and self.card is not None

    # --- 進行 ---
    def draw_once(self) -> Optional[int]:
        """1球引いてカードに反映。未開始/尽きた/ビンゴ12なら None。"""
        if not self.started():
            return None
        # すでに全ラインビンゴなら引かない
        if count_bingo(self.card.opened) == 12:  # type: ignore[union-attr]
            return None
        n = self.balls.draw()  # type: ignore[union-attr]
        if n is None:
            return None
        self.card.mark(n)      # type: ignore[union-attr]
        self.last = n
        return n

    # --- 表示用ステータス ---
    def status(self) -> Dict[str, Any]:
        if not self.started():
            return {"last": None, "drawn": 0, "remaining": 75, "reach": 0, "bingo": 0, "complete": False}
        reach = count_reach(self.card.opened)    # type: ignore[union-attr]
        bingo = count_bingo(self.card.opened)    # type: ignore[union-attr]
        return {
            "last": self.last,
            "drawn": self.balls.drawn(),         # type: ignore[union-attr]
            "remaining": self.balls.remaining(), # type: ignore[union-attr]
            "reach": reach,
            "bingo": bingo,
            "complete": (bingo == 12),
        }
