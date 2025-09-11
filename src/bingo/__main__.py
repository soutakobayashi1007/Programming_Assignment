from bingo.app import Session

HELP = "コマンド: n=New Game, d=Draw, r=Reset(白紙), s=Status, q=Quit"

def print_status(sess: Session) -> None:
    st = sess.status()
    if not sess.started():
        print("(カード未生成)")
        print(f"Drawn: {st['drawn']} | Remaining: {st['remaining']} | Reach: {st['reach']} | Bingo: {st['bingo']}")
        return
    print(sess.card.render())            # type: ignore[union-attr]
    print(f"Drawn: {st['drawn']} | Remaining: {st['remaining']} | Reach: {st['reach']} | Bingo: {st['bingo']}")

def main() -> None:
    sess = Session()

    print("=== BINGO ===")
    print_status(sess)
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
            sess.new_game()
            print("New Game started.")
            print_status(sess)
        elif s in ("r", "reset"):
            sess.reset_blank()
            print("白紙にリセットしました。")
            print_status(sess)
        elif s in ("d", "draw"):
            n = sess.draw_once()
            if n is None:
                st = sess.status()
                if not sess.started():
                    print("まず 'n' (New Game) を実行してください。")
                elif st["complete"]:
                    print("ビンゴが12に達しました。ゲーム終了です。")
                elif st["remaining"] == 0:
                    print("ボールはもうありません。")
                else:
                    print("引けませんでした。")
            else:
                print(f"Ball: {n}")
                print_status(sess)
        elif s in ("s", "status"):
            print_status(sess)
        else:
            print("不明なコマンド。 " + HELP)

if __name__ == "__main__":
    main()
