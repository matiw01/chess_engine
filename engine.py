from chess import Board
import chess as c


class Engine:
    def __init__(self, board=Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'),
                 player_colour=True, depth=4, quiescence=4):

        self.board = board
        self.player_colour = player_colour
        self.depth = depth
        self.quiescence = quiescence
        self.PIECE_VALUES = {
            c.PAWN: 1,
            c.KNIGHT: 3,
            c.BISHOP: 3,
            c.ROOK: 5,
            c.QUEEN: 9,
            c.KING: 0,
        }
        self.evaluated_positions = {}

    def make_move(self):
        move = self.calculate_move(self.depth)
        self.board.push(move)

    def get_outcome(self):
        outcome = self.board.outcome()
        if outcome is None:
            return None
        if outcome.termination == c.Termination.CHECKMATE and outcome.winner == self.player_colour:
            return float('-inf')
        if outcome.termination == c.Termination.CHECKMATE and not outcome.winner == self.player_colour:
            return float('inf')
        if outcome.termination == 0:
            return 0

    def evaluate_board(self):
        outcome = self.get_outcome()
        if outcome is not None:
            return outcome
        white = 0
        black = 0
        pieces = self.board.piece_map().values()
        for piece in pieces:
            if piece.color == c.WHITE:
                white += self.PIECE_VALUES[piece.piece_type]
            else:
                black += self.PIECE_VALUES[piece.piece_type]
        # static evaluation counting mobility but slowing engine X10
        # moves1 = len(list(self.board.legal_moves))
        # self.board.push(c.Move.null())
        # moves2 = len(list(self.board.legal_moves))
        # self.board.pop()
        # if self.board.turn == c.WHITE:
        #     white += moves1*0.001
        #     black += moves2*0.001
        # else:
        #     black += moves1*0.001
        #     white += moves2*0.001
        if not self.player_colour:
            return white - black
        return black - white

    def evaluate_move(self, move, colour):
        if self.board.gives_check(move):
            return 3
        if self.board.is_capture(move):
            if self.board.is_en_passant(move):
                if self.board.is_attacked_by(colour, move.to_square):
                    return 0
                else:
                    return 1
            if self.board.is_attacked_by(colour, move.to_square):
                return self.PIECE_VALUES[self.board.piece_at(move.to_square).piece_type] - self.PIECE_VALUES[
                    self.board.piece_at(move.from_square).piece_type]
            else:
                return self.PIECE_VALUES[self.board.piece_at(move.to_square).piece_type]
        return 0

    def sort_moves(self, moves: list, colour: c.Color):
        moves.sort(key=lambda x: self.evaluate_move(x, colour), reverse=True)

    def min_(self, alpha: float, beta: float, depth_left: int):
        if depth_left > 0:
            n = self.board.legal_moves.count()
            # checkmate and stalemate check
            if n == 0:
                if self.board.is_checkmate():
                    return float('inf'), alpha, beta
                if self.board.is_stalemate():
                    return 0, alpha, beta
            # looking for best move
            mini = float('inf')
            moves = self.board.generate_legal_moves()
            moves = list(moves)
            self.sort_moves(moves, not self.player_colour)
            for move in moves:
                self.board.push(move)
                value = self.max_(alpha, beta, depth_left - 1)[0]
                mini = min(mini, value)
                beta = min(beta, mini)
                self.board.pop()
                if alpha >= mini:
                    return mini, alpha, beta
            return mini, alpha, beta
        # print("Starting quisence serch")
        return self.quiescence_search_min(alpha, beta, self.quiescence)

    def max_(self, alpha: float, beta: float, depth_left: int):
        if depth_left > 0:
            n = self.board.legal_moves.count()
            if n == 0:
                if self.board.is_checkmate():
                    return float('-inf'), alpha, beta
                if self.board.is_stalemate():
                    return 0, alpha, beta
            maxi = float('-inf')
            moves = self.board.generate_legal_moves()
            moves = list(moves)
            self.sort_moves(moves, self.player_colour)
            for move in moves:
                self.board.push(move)
                value = self.min_(alpha, beta, depth_left - 1)[0]
                maxi = max(value, maxi)
                alpha = max(alpha, maxi)
                self.board.pop()
                if maxi >= beta:
                    return maxi, alpha, beta
            return maxi, alpha, beta
        # print("Starting quisence search")
        return self.quiescence_search_max(alpha, beta, self.quiescence)

    def calculate_move(self, depth_left: int):
        alpha = float('-inf')
        beta = float('inf')
        n = self.board.legal_moves.count()
        best_move = None
        maxi = float('-inf')
        moves = self.board.generate_legal_moves()
        moves = list(moves)
        self.sort_moves(moves, self.player_colour)
        for i in range(n):
            move = moves[i]
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
        print('position evaluation', maxi)
        return best_move

    def quiescence_search_min(self, alpha, beta, depth_left):
        if depth_left > 0:
            mini = float('inf')
            if not self.board.is_check():
                mini = self.evaluate_board()
                if mini <= alpha:
                    return mini, alpha, beta
                beta = min(beta, mini)
            n = self.board.legal_moves.count()
            if n == 0:
                if self.board.is_checkmate():
                    return float('inf'), alpha, beta
                if self.board.is_stalemate():
                    return 0, alpha, beta
            moves = self.board.generate_legal_moves()
            moves = list(moves)
            self.sort_moves(moves, not self.player_colour)
            for move in moves:
                if self.board.gives_check(move) or self.board.is_capture(move) or self.board.is_check():
                    self.board.push(move)
                    value = self.quiescence_search_max(alpha, beta, depth_left - 1)[0]
                    mini = min(value, mini)
                    beta = min(beta, mini)
                    self.board.pop()
                    if mini <= alpha:
                        return mini, alpha, beta
            return mini, alpha, beta
        return self.evaluate_board(), alpha, beta

    def quiescence_search_max(self, alpha, beta, depth_left):
        if depth_left > 0:
            maxi = float('-inf')
            if not self.board.is_check():
                maxi = self.evaluate_board()
                if maxi >= beta:
                    return maxi, alpha, beta
                alpha = max(alpha, maxi)
            n = self.board.legal_moves.count()
            if n == 0:
                if self.board.is_checkmate():
                    return float('-inf'), alpha, beta
                if self.board.is_stalemate():
                    return 0, alpha, beta
            moves = self.board.generate_legal_moves()
            moves = list(moves)
            self.sort_moves(moves, self.player_colour)
            for move in moves:
                if self.board.gives_check(move) or self.board.is_capture(move) or self.board.is_check():
                    self.board.push(move)
                    value = self.quiescence_search_min(alpha, beta, depth_left - 1)[0]
                    maxi = max(value, maxi)
                    alpha = max(alpha, maxi)
                    self.board.pop()
                    if maxi >= beta:
                        return maxi, alpha, beta
            return maxi, alpha, beta
        return self.evaluate_board(), alpha, beta

    def print(self):
        print(self.board, end="\n --------------\n")

        # symbols = ['Q', 'R', 'N', 'B', 'P']
        # values = [9, 5, 3, 3, 1]
        # for i in range(len(symbols)):
        #     white += len(self.board.pieces(c.Piece.from_symbol(symbols[i]).piece_type, c.WHITE)) * values[i]
        #     black += len(self.board.pieces(c.Piece.from_symbol(symbols[i]).piece_type, c.BLACK)) * values[i]
