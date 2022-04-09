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


engine = Engine(board=c.Board("r5rk/2p1Nppp/3p3P/pp2p1P1/4P3/2qnPQK1/8/R6R w - - 1 1"),
                player_colour=False, depth=4, quiescence=4)

engine_won = False
if engine.player_colour:
    engine.print()
    players_move()
    engine.print()
while not engine.board.is_checkmate() and not engine.board.is_stalemate():
    checkpoint = time()
    engine.make_move()
    print("Move made in ", time() - checkpoint, "s")
    engine.print()
    if engine.board.is_checkmate():
        engine_won = True
        print("You lost")
        break
    players_move()
    engine.print()
if not engine_won:
    print("You won")
