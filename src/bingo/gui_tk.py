from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional

from .balls import BingoBalls
from .card import BingoCard
from .result import count_reach, count_bingo

# ===== 表示用定数 =====
GRID = 5
CELL = 64  
FREE_BG = "#fecaca" 
OPEN_BG = "#a7f3d0" 
CLOSED_BG = "white" 
BORDER = "#9e9e9e"

class BingoApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Bingo (Tkinter)")
        self.resizable(False, False)

        # 起動直後は白紙（未開始）
        self.balls: Optional[BingoBalls] = None
        self.card:  Optional[BingoCard]  = None

        self._build_ui()
        self._update_all(last=None)

    # ---------- UI ----------
    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=12)
        root.grid(row=0, column=0, sticky="nsew")

        # 正方形の盤面（Canvas）
        size = CELL * GRID
        self.canvas = tk.Canvas(root, width=size, height=size,
                                highlightthickness=0, bg=CLOSED_BG)
        self.canvas.grid(row=0, column=0, rowspan=2)

        # 操作
        ctrl = ttk.Frame(root, padding=(12, 0))
        ctrl.grid(row=0, column=1, sticky="n")
        self.btn_draw = ttk.Button(ctrl, text="Draw (d)", command=self.on_draw)
        self.btn_draw.grid(row=0, column=0, sticky="ew")
        self.btn_draw.state(["disabled"])  # 未開始なので押せない

        ttk.Button(ctrl, text="New Game (n)", command=self.on_new).grid(
            row=1, column=0, sticky="ew", pady=6
        )
        ttk.Button(ctrl, text="Quit (q)", command=self.on_quit).grid(
            row=2, column=0, sticky="ew"
        )

        # ステータス
        stat = ttk.Frame(root, padding=(12, 8))
        stat.grid(row=1, column=1, sticky="nw")
        self.var_last = tk.StringVar()
        self.var_drawn = tk.StringVar()
        self.var_remain = tk.StringVar()
        self.var_reach = tk.StringVar()
        self.var_bingo = tk.StringVar()
        for v in (self.var_last, self.var_drawn, self.var_remain, self.var_reach, self.var_bingo):
            ttk.Label(stat, textvariable=v).pack(anchor="w")

        # キーボードショートカット
        self.bind("<Key-d>", lambda e: self.on_draw())
        self.bind("<Key-n>", lambda e: self.on_new())
        self.bind("<Key-q>", lambda e: self.on_quit())

    # ---------- 動作 ----------
    def on_new(self) -> None:
        self.balls = BingoBalls()
        self.card = BingoCard.from_random()
        self.btn_draw.state(["!disabled"])
        self._update_all(last=None)

    def on_draw(self) -> None:
        if self.balls is None or self.card is None:
            return  # 未開始
        n = self.balls.draw()
        if n is None:
            self.btn_draw.state(["disabled"])
            return
        self.card.mark(n)
        self._update_all(last=n)
        if self.balls.remaining() == 0:
            self.btn_draw.state(["disabled"])

    def on_quit(self) -> None:
        self.destroy()

    # ---------- 表示更新 ----------
    def _cell_rect(self, r: int, c: int) -> tuple[int, int, int, int]:
        x0 = c * CELL
        y0 = r * CELL
        return x0, y0, x0 + CELL, y0 + CELL

    def _draw_board(self, started: bool) -> None:
        self.canvas.delete("all")
        for r in range(GRID):
            for c in range(GRID):
                x0, y0, x1, y1 = self._cell_rect(r, c)
                if not started:
                    fill = CLOSED_BG
                    text = ""
                else:
                    n = self.card.grid[r][c]          # type: ignore[union-attr]
                    opened = self.card.opened[r][c]   # type: ignore[union-attr]
                    if n is None:
                        fill, text = FREE_BG, "FREE"
                    else:
                        fill, text = (OPEN_BG, str(n)) if opened else (CLOSED_BG, str(n))

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline=BORDER, width=1)
                if text:
                    self.canvas.create_text(
                        (x0 + x1) // 2, (y0 + y1) // 2,
                        text=text, font=("Segoe UI", 14, "bold")
                    )

    def _update_all(self, last: Optional[int]) -> None:
        started = (self.balls is not None) and (self.card is not None)
        self._draw_board(started)

        drawn  = 0 if not started else self.balls.drawn()        # type: ignore[union-attr]
        remain = 75 if not started else self.balls.remaining()   # type: ignore[union-attr]
        reach  = 0 if not started else count_reach(self.card.opened)  # type: ignore[union-attr]
        bingo  = 0 if not started else count_bingo(self.card.opened)  # type: ignore[union-attr]

        self.var_last.set(f"Last: {last if last is not None else '-'}")
        self.var_drawn.set(f"Drawn: {drawn}")
        self.var_remain.set(f"Remaining: {remain}")
        self.var_reach.set(f"Reach: {reach}")
        self.var_bingo.set(f"Bingo: {bingo}")

def main() -> None:
    app = BingoApp()
    app.mainloop()

if __name__ == "__main__":
    main()
