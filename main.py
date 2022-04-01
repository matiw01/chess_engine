import chess as c
from engine import Engine


def players_move():
    while True:
        move = input("Podaj ruch: ")
        move = c.Move.from_uci(move)
        if move in engine.board.generate_legal_moves():
            engine.board.push(move)
            break
        else:
            print("move is not valid")


engine = Engine(True, 3)


if engine.colour:
    print(engine.board, end="\n --------------\n")
    players_move()
    print(engine.board, end="\n --------------\n")
while not engine.board.is_checkmate() and not engine.board.is_stalemate():
    engine.make_move()
    print(engine.board, end="\n --------------\n")
    players_move()
    print(engine.board, end="\n --------------\n")
