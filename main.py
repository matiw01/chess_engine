import chess as c
from engine import Engine
from engine2 import Engine2
from minMax import calculate_move_naive


def players_move():
    while True:
        move = input("Pass your move: ")
        move = c.Move.from_uci(move)
        if move in engine.board.generate_legal_moves():
            engine.board.push(move)
            break
        else:
            print("move is not valid")


engine = Engine(True, 4)

if engine.colour:
    engine.print()
    players_move()
    engine.print()
while not engine.board.is_checkmate() and not engine.board.is_stalemate():
    engine.make_move()
    engine.print()
    players_move()
    engine.print()
