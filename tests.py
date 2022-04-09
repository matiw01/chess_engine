import chess as c
from engine import Engine
from time import time

tests = ["r2qkb1r/pbpppppp/1pn3n1/4B3/4P3/2NP2Q1/PPP2PPP/RN2KB1R w KQkq - 0 1",  #checks if takes piece defended by stronger piece
         "r1bqkb1r/pppppppp/2n5/6NQ/4P3/2NP4/PPP2PPP/R3KB1R w KQkq - 0 1",  # mate + some trades after defending
         "4k3/n1b1pppp/8/4q3/3p4/3P1N2/PPP2PPP/5RK1 w - - 0 1",  #checks if engine prfers to get free material or mate in 1
         "r1b1kb1r/pppp1ppp/5q2/4n3/3KP3/2N3PN/PPP4P/R1BQ1B1R b kq - 0 1", # mate in 3 with material sacrifice
         "r5rk/2p1Nppp/3p3P/pp2p1P1/4P3/2qnPQK1/8/R6R w - - 1 1", # mate in 4 with material sacrifice -> problem with engine evaluating mate in n moves and mate in n-1 moves same
         "2bqkbnr/P1pppppp/8/8/8/8/1PPPPPPP/RNBQKBNR b KQk - 0 1", #checks if can promote
         "2bqkbnr/P1pppppp/8/8/8/8/1PPPPPPP/RNBQKBNR w KQk - 0 1", #checks if can defend promotion field
         "r3k1nr/pppqb1pp/2n1ppb1/3pP2P/3P4/P1NB1N2/1PP2PP1/R1BQ1RK1 w Qkq - 0 1", #optimization test with little change
         "r3k1nr/pppqb1pp/2n1ppb1/3pP3/3P4/P1NB1N2/1PP2PPP/R1BQ1RK1 w Qkq - 0 1"] , #optimization test

board = c.Board("r1b1k2r/pppp1ppp/3q4/3Kn3/4P3/2N3PN/PPP4P/R1BQ1B1R w kq - 3 4")

engine = Engine(board=c.Board("r1b1k2r/pppp1ppp/3q4/3Kn3/4P3/2N3PN/PPP4P/R1BQ1B1R w kq - 3 4"), player_colour=c.WHITE)
engine.print()
# print(engine.evaluate())


# print(engine.evaluate())

# print(board.piece_map().values())
# checkpoint = time()
# print("time:", time()-checkpoint)

checkpoint = time()
for i in range(10000):
    engine.evaluate_board()
print(time() - checkpoint)


def CapturedPiece(board, move):
    if board.is_capture(move):
        if board.is_en_passant(move):
            return 1
        else:
            return board.piece_at(move.to_square).piece_type
    return 0
