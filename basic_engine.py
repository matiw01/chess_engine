from chess import Board
import chess as c


class Engine2:
    def __init__(self, colour: bool, depth: int):
        self.board = Board()
        self.colour = colour
        self.depth = depth

    def make_move(self):
        move = self.calculate_move(self.depth)
        self.board.push(move)

    def evaluate(self):
        white = 0
        black = 0
        symbols = ['Q', 'R', 'N', 'B', 'P']
        values = [9, 5, 3, 3, 1]
        for i in range(len(symbols)):
            white += len(self.board.pieces(c.Piece.from_symbol(symbols[i]).piece_type, True)) * values[i]
            black += len(self.board.pieces(c.Piece.from_symbol(symbols[i]).piece_type, False)) * values[i]
        if not self.colour:
            return white - black
        return black - white

    def min_(self, depth_left: int):
        if depth_left > 0:
            n = self.board.legal_moves.count()
            if n == 0:
                if self.board.is_checkmate():
                    return float('-inf')
            D = [float('inf') for _ in range(n)]
            moves = self.board.generate_legal_moves()
            for i in range(n):
                move = next(moves)
                self.board.push(move)
                D[i] = self.max_(depth_left - 1)
                self.board.pop()
            return min(D)
        return self.evaluate()

    def max_(self, depth_left: int):
        if depth_left > 0:
            n = self.board.legal_moves.count()
            if n == 0:
                if self.board.is_checkmate():
                    return float('inf')
            D = [float('inf') for _ in range(n)]
            moves = self.board.generate_legal_moves()
            for i in range(n):
                move = next(moves)
                self.board.push(move)
                D[i] = self.min_(depth_left - 1)
                self.board.pop()
            return max(D)
        return self.evaluate()

    def calculate_move(self, depth_left: int):
        n = self.board.legal_moves.count()
        D = [[float('-inf'), None] for _ in range(n)]
        moves = self.board.generate_legal_moves()
        for i in range(n):
            move = next(moves)
            self.board.push(move)
            D[i][0] = self.min_(depth_left - 1)
            D[i][1] = move
            self.board.pop()
        best_value = float('-inf')
        best_valued_move = None
        for i in range(n):
            if D[i][0] > best_value:
                best_value = D[i][0]
                best_valued_move = D[i][1]
        print(best_valued_move, best_value)
        return best_valued_move

    def print(self):
        print(self.board, end="\n --------------\n")