from chess import Move
from chess import Board

board = Board()
# print(board.fen())
moves = board.generate_legal_moves()
print(type(moves))
# for move in moves:
#     print(move)
for _ in range(10):
    pass