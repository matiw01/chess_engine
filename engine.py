from chess import Board
import chess as c


class Engine:
    def __init__(self, colour: bool, depth: int):
        self.board = Board()
        self.colour = colour
        self.depth = depth

    def make_move(self):
        move = self.calculate_move(self.depth)
        self.board.push(move)

    def evaluate(self):
        if self.board.is_checkmate() and self.depth % 2 == 0:
            return float('-inf')
        if self.board.is_checkmate() and self.depth % 2 == 1:
            return float('inf')
        if self.board.is_stalemate():
            return 0
        white = 0
        black = 0
        symbols = ['Q', 'R', 'N', 'B', 'P']
        values = [9, 5, 3, 3, 1]
        for i in range(len(symbols)):
            white += len(self.board.pieces(c.Piece.from_symbol(symbols[i]).piece_type, c.WHITE)) * values[i]
            black += len(self.board.pieces(c.Piece.from_symbol(symbols[i]).piece_type, c.BLACK)) * values[i]
        if not self.colour:
            return white - black
        return black - white

    def min_(self, alpha: float, beta: float, depth_left: int):
        if depth_left > 0:
            n = self.board.legal_moves.count()
            # checkmate and stalemate check
            if n == 0:
                if self.board.is_checkmate():
                    return float('-inf'), alpha, beta
                if self.board.is_stalemate():
                    return 0, alpha, beta
            # looking for best move
            mini = float('inf')
            moves = self.board.generate_legal_moves()
            for i in range(n):
                move = next(moves)
                self.board.push(move)
                value = self.max_(alpha, beta, depth_left - 1)[0]
                mini = min(mini, value)
                beta = min(beta, mini)
                self.board.pop()
                if alpha >= mini:
                    return mini, alpha, beta
            return mini, alpha, beta
        return self.evaluate(), alpha, beta

    def max_(self, alpha: float, beta: float, depth_left: int):
        if depth_left > 0:
            n = self.board.legal_moves.count()
            if n == 0:
                if self.board.is_checkmate():
                    return float('inf'), alpha, beta
                if self.board.is_stalemate():
                    return 0, alpha, beta
            maxi = float('-inf')
            moves = self.board.generate_legal_moves()
            for i in range(n):
                move = next(moves)
                self.board.push(move)
                value = self.min_(alpha, beta, depth_left - 1)[0]
                maxi = max(value, maxi)
                alpha = max(alpha, maxi)
                self.board.pop()
                if maxi >= beta:
                    return maxi, alpha, beta
            return maxi, alpha, beta
        return self.evaluate(), alpha, beta

    def calculate_move(self, depth_left: int):
        alpha = float('-inf')
        beta = float('inf')
        n = self.board.legal_moves.count()
        best_move = None
        maxi = float('-inf')
        moves = self.board.generate_legal_moves()
        for i in range(n):
            move = next(moves)
            self.board.push(move)
            value = self.min_(alpha, beta, depth_left - 1)[0]
            if maxi < value:
                maxi = value
                best_move = move
            self.board.pop()
            alpha = max(alpha, maxi)
            # print("for move {} got {}".format(move, value))
            if maxi > beta:
                # print('value by alpha', maxi)
                return best_move
        # print('value', maxi)
        return best_move

    def print(self):
        print(self.board, end="\n --------------\n")
