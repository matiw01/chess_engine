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


engine = Engine(board=c.Board("r3k1nr/pppqb1pp/2n1ppb1/3pP3/3P4/P1NB1N2/1PP2PPP/R1BQ1RK1 w Qkq - 0 1"),
                player_colour=True, depth=2, quiescence=6)

engine_won = False
if engine.player_colour:
    engine.print()
    players_move()
    engine.print()
while not engine.board.is_checkmate() and not engine.board.is_stalemate():
    checkpoint = time()
    engine.make_move()
    print("Move made in ", time() - checkpoint, "s")
    print("Used dictionary", engine.used_dictionary)
    print("There are {} values in dictionary".format(len(engine.evaluated_positions)))
    print("Visited {}".format(engine.visited_nodes))
    engine.print()
    if engine.board.is_checkmate():
        engine_won = True
        print("You lost")
        break
    players_move()
    engine.print()
if not engine_won:
    print("You won")
