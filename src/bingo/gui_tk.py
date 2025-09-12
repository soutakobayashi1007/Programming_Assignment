from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional

from .app import Session

# 定数定義: ゲームの表示設定
GRID = 5
CELL = 64
FREE_BG = "#fecaca"  # FREEマスの背景色
OPEN_BG = "#a7f3d0"  # 開いたマスの背景色
CLOSED_BG = "white"  # 開いていないマスの背景色
BORDER = "black"  # マス間のボーダー色

class BingoApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Bingo (Tkinter)")  # ウィンドウタイトルを設定
        self.resizable(False, False)   # ウィンドウのリサイズを禁止
        self.sess = Session()          # ゲームセッションを初期化（未開始状態）
        self._build_ui()               # UIを構築
        self._update_all()             # 初期表示を更新

    def _build_ui(self) -> None:
        # ルートフレームを作成し、パディングを追加
        root = ttk.Frame(self, padding=12)
        root.grid(row=0, column=0, sticky="nsew")

        # キャンバスのサイズを計算し、作成
        size = CELL * GRID
        self.canvas = tk.Canvas(root, width=size, height=size, highlightthickness=0, bg=CLOSED_BG)
        self.canvas.grid(row=0, column=0, rowspan=2)  # キャンバスを配置

        # コントロールフレームを作成し、ボタンを配置
        ctrl = ttk.Frame(root, padding=(12, 0))
        ctrl.grid(row=0, column=1, sticky="n")
        self.btn_draw = ttk.Button(ctrl, text="Draw (d)", command=self.on_draw)
        self.btn_draw.grid(row=0, column=0, sticky="ew")  # ドローボタンを配置
        self.btn_draw.state(["disabled"])  # 初期状態でボタンを無効化
        ttk.Button(ctrl, text="New Game (n)", command=self.on_new).grid(
            row=1, column=0, sticky="ew", pady=6  # 新規ゲームボタンを配置
        )
        ttk.Button(ctrl, text="Quit (q)", command=self.on_quit).grid(row=2, column=0, sticky="ew")  # 終了ボタンを配置

        # ステータス表示フレームを作成し、ラベルを追加
        stat = ttk.Frame(root, padding=(12, 8))
        stat.grid(row=1, column=1, sticky="nw")
        self.var_last = tk.StringVar()
        self.var_drawn = tk.StringVar()
        self.var_remain = tk.StringVar()
        self.var_reach = tk.StringVar()
        self.var_bingo = tk.StringVar()
        for v in (self.var_last, self.var_drawn, self.var_remain, self.var_reach, self.var_bingo):
            ttk.Label(stat, textvariable=v).pack(anchor="w")  # 各ステータスを左寄せで表示

        # キーボードショートカットを設定
        self.bind("<Key-n>", lambda e: self.on_new())
        self.bind("<Key-d>", lambda e: self.on_draw())
        self.bind("<Key-q>", lambda e: self.on_quit())

    # --- 動作処理 ---
    def on_new(self) -> None:
        self.sess.new_game()       # 新しいゲームを開始
        self._update_all()         # 画面を更新

    def on_draw(self) -> None:
        self.sess.draw_once()      # 1球引く
        self._update_all()         # 画面を更新

    def on_quit(self) -> None:
        self.destroy()             # ウィンドウを閉じる

    # --- 表示更新処理 ---
    def _cell_rect(self, r: int, c: int) -> tuple[int, int, int, int]:
        # マスの左上と右下の座標を計算
        x0 = c * CELL
        y0 = r * CELL
        return x0, y0, x0 + CELL, y0 + CELL

    def _draw_board(self) -> None:
        self.canvas.delete("all")  # キャンバスをクリア
        started = self.sess.started()  # ゲーム開始状態を確認
        for r in range(GRID):
            for c in range(GRID):
                # 各マスの矩形座標を取得
                x0, y0, x1, y1 = self._cell_rect(r, c)
                if not started:
                    fill, text = CLOSED_BG, ""  # 未開始時は白背景で空
                else:
                    n = self.sess.card.grid[r][c]     # マスの数字を取得
                    opened = self.sess.card.opened[r][c]  # マスの開閉状態
                    if n is None:
                        fill, text = FREE_BG, "FREE"
                    else:
                        fill, text = (OPEN_BG, str(n)) if opened else (CLOSED_BG, str(n))  # 開/閉で色変更
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline=BORDER, width=1)  # 矩形を描画
                if text:
                    self.canvas.create_text(
                        (x0 + x1) // 2, (y0 + y1) // 2, text=text, font=("Segoe UI", 14, "bold")
                    )  # テキストを中央に配置

    def _update_all(self) -> None:
        self._draw_board()  # ボードを再描画
        st = self.sess.status()  # ゲームステータスを取得
        self.var_last.set(f"Last: {st['last'] if st['last'] is not None else '-'}")  # 最後の数字更新
        self.var_drawn.set(f"Drawn: {st['drawn']}")  # 引いた数更新
        self.var_remain.set(f"Remaining: {st['remaining']}")  # 残り数更新
        self.var_reach.set(f"Reach: {st['reach']}")  # リーチ数更新
        self.var_bingo.set(f"Bingo: {st['bingo']}")  # ビンゴ数更新
        # ボタンの有効/無効を制御（未開始/ボール0/ビンゴ12で無効）
        if (not self.sess.started()) or st["remaining"] == 0 or st["complete"]:
            self.btn_draw.state(["disabled"])
        else:
            self.btn_draw.state(["!disabled"])

def main() -> None:
    app = BingoApp()
    app.mainloop()

if __name__ == "__main__":
    main()