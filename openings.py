

import chess.polyglot

board = chess.Board()
reader = chess.polyglot.open_reader("opening_base/bookoutput.bin")
print(type(reader.find_all(board)))