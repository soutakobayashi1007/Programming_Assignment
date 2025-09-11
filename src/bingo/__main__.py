from bingo.balls import BingoBalls
from bingo.card import BingoCard
from bingo.result import count_reach, count_bingo

HELP = "コマンド: d=次のボール, m <数字>=手動マーク, r=新しいカード, q=終了"

def _print_status(card: BingoCard, balls: BingoBalls) -> None:
    reach = count_reach(card.opened)
    bingo = count_bingo(card.opened)
    print(card.render())
    print(f"Reach: {reach} / Bingo: {bingo}  |  残りボール: {balls.remaining()}")

def main() -> None:
    balls = BingoBalls()
    card = BingoCard.from_random()

    print("=== BINGO ===")
    _print_status(card, balls)
    print("\n" + HELP + "\n")

    while True:
        try:
            s = input("> ").strip()
        except EOFError:
            break
        if not s:
            continue

        parts = s.split()
        cmd = parts[0].lower()

        if cmd in ("q", "quit", "exit"):
            break

        elif cmd in ("d", "draw"):
            n = balls.draw()
            if n is None:
                print("ボールはもうありません。")
            else:
                card.mark(n)
                print(f"Ball: {n}")
                _print_status(card, balls)

        elif cmd in ("m", "mark"):
            if len(parts) < 2 or not parts[1].isdigit():
                print("使い方: m <数字>")
                continue
            n = int(parts[1])
            changed = card.mark(n)
            print("marked" if changed else "not found / already open")
            _print_status(card, balls)

        elif cmd in ("r", "reset"):
            balls = BingoBalls()
            card = BingoCard.from_random()
            print("新しいカードを作成しました。")
            _print_status(card, balls)

        else:
            print("不明なコマンド。 " + HELP)

if __name__ == "__main__":
    main()
