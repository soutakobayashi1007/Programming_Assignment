# Bingo (Assignment)

## セットアップ
1. 仮想環境: `python -m venv .venv`（Windows: `py -3.12.4 -m venv .venv`）
2. 有効化: `source .venv/bin/activate`（Windows: `.venv\Scripts\activate`）
3. 開発ツール: `pip install -U pip && pip install -r requirements-dev.txt`

## よく使うコマンド
- テスト: `pytest`
- Lint: `ruff check src tests`
- フォーマット: `black src tests`
- 実行: `python -m bingo`
