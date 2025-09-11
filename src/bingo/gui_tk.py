from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional

from .app import Session

GRID = 5
CELL = 64
FREE_BG = "#fecaca"   # FREE（薄赤）
OPEN_BG = "#a7f3d0"   # 開マス（薄緑）
CLOSED_BG = "white"
BORDER = "#9e9e9e"

class BingoApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Bingo (Tkinter)")
        self.resizable(False, False)

        self.sess = Session()  # 起動直後は未開始

        self._build_ui()
        self._update_all()

    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=12); root.grid(row=0, column=0, sticky="nsew")

        size = CELL * GRID
        self.canvas = tk.Canvas(root, width=size, height=size, highlightthickness=0, bg=CLOSED_BG)
        self.canvas.grid(row=0, column=0, rowspan=2)

        ctrl = ttk.Frame(root, padding=(12, 0)); ctrl.grid(row=0, column=1, sticky="n")
        self.btn_draw = ttk.Button(ctrl, text="Draw (d)", command=self.on_draw); self.btn_draw.grid(row=0, column=0, sticky="ew")
        self.btn_draw.state(["disabled"])
        ttk.Button(ctrl, text="New Game (n)", command=self.on_new).grid(row=1, column=0, sticky="ew", pady=6)
        ttk.Button(ctrl, text="Quit (q)", command=self.on_quit).grid(row=2, column=0, sticky="ew")

        stat = ttk.Frame(root, padding=(12, 8)); stat.grid(row=1, column=1, sticky="nw")
        self.var_last   = tk.StringVar()
        self.var_drawn  = tk.StringVar()
        self.var_remain = tk.StringVar()
        self.var_reach  = tk.StringVar()
        self.var_bingo  = tk.StringVar()
        for v in (self.var_last, self.var_drawn, self.var_remain, self.var_reach, self.var_bingo):
            ttk.Label(stat, textvariable=v).pack(anchor="w")

        # ショートカット
        self.bind("<Key-n>", lambda e: self.on_new())
        self.bind("<Key-d>", lambda e: self.on_draw())
        self.bind("<Key-q>", lambda e: self.on_quit())

    # --- 動作 ---
    def on_new(self) -> None:
        self.sess.new_game()
        self._update_all()

    def on_draw(self) -> None:
        n = self.sess.draw_once()
        self._update_all()

    def on_quit(self) -> None:
        self.destroy()

    # --- 表示更新 ---
    def _cell_rect(self, r: int, c: int) -> tuple[int, int, int, int]:
        x0 = c * CELL; y0 = r * CELL
        return x0, y0, x0 + CELL, y0 + CELL

    def _draw_board(self) -> None:
        self.canvas.delete("all")
        started = self.sess.started()
        for r in range(GRID):
            for c in range(GRID):
                x0, y0, x1, y1 = self._cell_rect(r, c)
                if not started:
                    fill, text = CLOSED_BG, ""
                else:
                    n = self.sess.card.grid[r][c]          # type: ignore[union-attr]
                    opened = self.sess.card.opened[r][c]   # type: ignore[union-attr]
                    if n is None:
                        fill, text = FREE_BG, "FREE"
                    else:
                        fill, text = (OPEN_BG, str(n)) if opened else (CLOSED_BG, str(n))
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline=BORDER, width=1)
                if text:
                    self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=text, font=("Segoe UI", 14, "bold"))

    def _update_all(self) -> None:
        self._draw_board()
        st = self.sess.status()
        self.var_last.set(f"Last: {st['last'] if st['last'] is not None else '-'}")
        self.var_drawn.set(f"Drawn: {st['drawn']}")
        self.var_remain.set(f"Remaining: {st['remaining']}")
        self.var_reach.set(f"Reach: {st['reach']}")
        self.var_bingo.set(f"Bingo: {st['bingo']}")
        # 停止条件: 未開始 / 残り0 / ビンゴ12
        if (not self.sess.started()) or st["remaining"] == 0 or st["complete"]:
            self.btn_draw.state(["disabled"])
        else:
            self.btn_draw.state(["!disabled"])

def main() -> None:
    app = BingoApp()
    app.mainloop()

if __name__ == "__main__":
    main()
