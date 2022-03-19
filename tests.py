from chess import Move
from chess import Board
from random import randint
import chess

board = Board()
# print(board.fen())
moves = board.generate_legal_moves()
print(type(moves))
# for move in moves:
#     print(move)
for _ in range(10):
    moves = board.generate_legal_moves()
    i = randint(1, board.legal_moves.count())
    for _ in range(i):
        uci = next(moves)
    board.push(uci)
    print(board)
    print("---------------")



