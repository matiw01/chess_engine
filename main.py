import chess as c
from engine import Engine
from time import time


def players_move():
    while True:
        move = input("Pass your move: ")
        try:
            move = c.Move.from_uci(move)
            if move in engine.board.generate_legal_moves():
                engine.board.push(move)
                break
            else:
                print("move is not valid")
        except ValueError:
            print("Your move should be in uci form")


engine = Engine(board=c.Board("r1b1kb1r/pppp1ppp/5q2/4n3/3KP3/2N3PN/PPP4P/R1BQ1B1R b kq - 0 1"),
                player_colour=True, depth=4, quiescence=4)

engine.print()
# if engine.player_colour:
#     engine.print()
#     players_move()
#     engine.print()
while not engine.board.is_checkmate() and not engine.board.is_stalemate():
    checkpoint = time()
    engine.make_move()
    print("Move made in ", time() - checkpoint, "s")
    engine.print()
    if engine.board.is_checkmate():
        print("You lost")
        break
    players_move()
    engine.print()
