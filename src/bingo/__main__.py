from bingo.balls import BingoBalls
from bingo.card import BingoCard
from bingo.result import count_reach, count_bingo

HELP = "コマンド: n=New Game, d=Draw, r=Reset(白紙), s=Status, q=Quit"

def _print_status(card, balls):
    if card is None or balls is None:
        print("(カード未生成)")
        return
    reach = count_reach(card.opened)
    bingo  = count_bingo(card.opened)
    print(card.render())
    print(f"Drawn: {balls.drawn()} | Remaining: {balls.remaining()} | Reach: {reach} | Bingo: {bingo}")

def main() -> None:
    balls = None
    card  = None

    print("=== BINGO ===")
    _print_status(card, balls)
    print("\n" + HELP + "\n")

    while True:
        try:
            s = input("> ").strip().lower()
        except EOFError:
            break
        if not s:
            continue

        if s in ("q", "quit", "exit"):
            break
        elif s in ("n", "new"):
            balls = BingoBalls()
            card  = BingoCard.from_random()
            print("New Game started.")
            _print_status(card, balls)
        elif s in ("r", "reset"):
            balls = None
            card  = None
            print("白紙にリセットしました。")
            _print_status(card, balls)
        elif s in ("d", "draw"):
            if balls is None or card is None:
                print("まず 'n' (New Game) を実行してください。")
                continue
            n = balls.draw()
            if n is None:
                print("ボールはもうありません。")
                continue
            card.mark(n)
            print(f"Ball: {n}")
            _print_status(card, balls)
        elif s in ("s", "status"):
            _print_status(card, balls)
        else:
            print("不明なコマンド。 " + HELP)

if __name__ == "__main__":
    main()
