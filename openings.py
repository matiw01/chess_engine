
import chess as c
import chess.polyglot

board = chess.Board()

pieces = board.piece_map()
# print(pieces)

pawns = board.pieces(c.Piece.from_symbol('P').piece_type, True)



