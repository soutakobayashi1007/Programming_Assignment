# Bingo Game

Python（標準ライブラリのみ）で動作するビンゴゲーム。

## 概要
- 5×5のビンゴカード（中央はFREE）
- 1〜75の数字を重複なく抽選
- ビンゴが12本になったらゲーム停止
- 起動直後は白紙、New Gameでゲーム開始

## 必要条件
- **Python**: 3.11〜3.13
- **Tkinter**: 通常はPythonに同梱

## セットアップ
プロジェクト直下で以下のコマンドを実行：

```bash
# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass # PowerShellでスクリプト実行を許可（セッション終了でリセット）
.\.venv\Scripts\Activate.ps1
# Windows (cmd)
.venv\Scripts\activate.bat

# pipのアップグレード
python -m pip install --upgrade pip

# プロジェクトのインストール
pip install -e .
```

## 実行方法

### CUI
```bash
python -m bingo
```
**操作**:
- `n`: New Game
- `d`: Draw
- `q`: Quit

### GUI (Tkinter)
```bash
python -m bingo.gui_tk
```
**ショートカット**:
- `n`: New Game
- `d`: Draw
- `q`: Quit




## 開発者向け

### テスト用環境のセットアップと実行
このプロジェクトでは、pytestをテストフレームワークとして使用し、ruff（linter）とblack（formatter）でコード品質を管理しています。開発依存は`requirements-dev.txt`に記載されており、`pyproject.toml`でpytestの設定を定義しています（例: 簡易出力`-q`、テストパス`tests/`）。

#### 1. 開発依存のインストール
仮想環境をアクティブ化した後、以下のコマンドでインストール：
```bash
pip install -r requirements-dev.txt
```