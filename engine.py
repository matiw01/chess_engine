import random

from chess import Board
import chess as c
import chess.polyglot


def pawns_advancement(pawns, param):
    sum_ = 0
    for pawn in pawns:
        sum_ += pawn // 8
    return sum_ * param


class Engine:
    def __init__(self, board=Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'),
                 player_colour=True, depth=2, quiescence=6):
        self.visited_nodes = 0
        self.used_dictionary = 0
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
        self.reader = chess.polyglot.open_reader("opening_base/bookoutput.bin")

    def make_move(self):
        opening_moves = (list(self.reader.find_all(self.board)))
        if len(opening_moves) != 0:
            self.board.push(random.choice(opening_moves).move)
            return
        self.evaluated_positions = {}
        move = self.calculate_move(self.depth)
        self.board.push(move)

    def get_outcome(self, depth_left):
        outcome = self.board.outcome()
        if outcome is None:
            return None
        if outcome.termination == c.Termination.CHECKMATE and outcome.winner == self.player_colour:
            return -1000 * depth_left
        if outcome.termination == c.Termination.CHECKMATE and not outcome.winner == self.player_colour:
            return 1000 * depth_left
        if outcome.termination == 0:
            return 0

    def evaluate_board(self, depth_left, moves1):
        self.visited_nodes += 1
        key = (c.polyglot.zobrist_hash(self.board), depth_left)
        if key in self.evaluated_positions:
            self.used_dictionary += 1
            return self.evaluated_positions[key]
        outcome = self.get_outcome(depth_left)
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

        self.board.push(c.Move.null())
        moves2 = len(list(self.board.legal_moves))
        self.board.pop()

        w_pawns = self.board.pieces(c.Piece.from_symbol('P').piece_type, True)
        b_pawns = self.board.pieces(c.Piece.from_symbol('P').piece_type, False)

        white += pawns_advancement(w_pawns, 0.01)
        black += pawns_advancement(b_pawns, 0.01)

        if self.board.turn == c.WHITE:
            white += moves1 * 0.01
            black += moves2 * 0.01
        else:
            black += moves1 * 0.01
            white += moves2 * 0.01

        if not self.player_colour:
            self.evaluated_positions[key] = round(white - black, 1)
            return round(white - black, 1)
        self.evaluated_positions[key] = round(black - white, 1)
        return round(black - white, 1)

    def evaluate_move(self, move, colour):
        if move.promotion is not None:
            return 8
        if self.board.gives_check(move):
            return 3
        if self.board.is_capture(move):
            if self.board.is_en_passant(move):
                if self.board.is_attacked_by(colour, move.to_square):
                    return 0
                else:
                    return 1
            if self.board.is_attacked_by(colour, move.to_square):
                return self.PIECE_VALUES[self.board.piece_at(move.to_square).piece_type] - \
                       self.PIECE_VALUES[self.board.piece_at(move.from_square).piece_type]
            else:
                return self.PIECE_VALUES[self.board.piece_at(move.to_square).piece_type]
        if self.board.is_castling(move):
            return 1
        return 0

    def sort_moves(self, moves: list, colour: c.Color):
        moves.sort(key=lambda x: self.evaluate_move(x, colour), reverse=True)

    def min_(self, alpha: float, beta: float, depth_left: int):
        if depth_left > 0:
            key = (c.polyglot.zobrist_hash(self.board), self.depth - depth_left)
            if key in self.evaluated_positions:
                self.used_dictionary += 1
                return self.evaluated_positions[key]
            self.visited_nodes += 1
            n = self.board.legal_moves.count()
            # checkmate and stalemate check
            if n == 0:
                if self.board.is_checkmate():
                    return 1000 * (depth_left + self.quiescence)
                if self.board.is_stalemate():
                    return 0
            # looking for best move
            mini = float('inf')
            moves = self.board.generate_legal_moves()
            moves = list(moves)
            self.sort_moves(moves, not self.player_colour)
            for move in moves:
                self.board.push(move)
                value = self.max_(alpha, beta, depth_left - 1)
                mini = min(mini, value)
                beta = min(beta, mini)
                self.board.pop()
                if alpha >= mini:
                    self.evaluated_positions[key] = mini
                    return mini
            self.evaluated_positions[key] = mini
            return mini
        return self.quiescence_search_min(alpha, beta, self.quiescence)

    def max_(self, alpha: float, beta: float, depth_left: int):
        if depth_left > 0:
            key = (c.polyglot.zobrist_hash(self.board), self.depth - depth_left)
            if key in self.evaluated_positions:
                self.used_dictionary += 1
                return self.evaluated_positions[key]
            self.visited_nodes += 1
            n = self.board.legal_moves.count()
            if n == 0:
                if self.board.is_checkmate():
                    return -1000 * (depth_left + self.quiescence)
                if self.board.is_stalemate():
                    return 0
            maxi = float('-inf')
            moves = self.board.generate_legal_moves()
            moves = list(moves)
            self.sort_moves(moves, self.player_colour)
            for move in moves:
                self.board.push(move)
                value = self.min_(alpha, beta, depth_left - 1)
                maxi = max(value, maxi)
                alpha = max(alpha, maxi)
                self.board.pop()
                if maxi >= beta:
                    self.evaluated_positions[key] = maxi
                    return maxi
            self.evaluated_positions[key] = maxi
            return maxi
        return self.quiescence_search_max(alpha, beta, self.quiescence)

    def calculate_move(self, depth_left: int):
        self.visited_nodes = 0
        self.used_dictionary = 0
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
            value = self.min_(alpha, beta, depth_left - 1)
            if maxi < value:
                maxi = value
                best_move = move
            self.board.pop()
            alpha = max(alpha, maxi)
            if maxi >= beta:
                return best_move
        print('position evaluation', maxi)
        return best_move

    def quiescence_search_min(self, alpha, beta, depth_left):
        moves = self.board.generate_legal_moves()
        moves = list(moves)
        if depth_left > 0:
            self.visited_nodes += 1
            mini = float('inf')

            if not self.board.is_check():
                mini = self.evaluate_board(depth_left, len(moves))
                if mini <= alpha:
                    return mini
                beta = min(beta, mini)
            n = self.board.legal_moves.count()
            if n == 0:
                if self.board.is_checkmate():
                    return 1000 * depth_left
                if self.board.is_stalemate():
                    return 0
            self.sort_moves(moves, not self.player_colour)
            for move in moves:
                if self.board.gives_check(move) or self.board.is_capture(move) or self.board.is_check():
                    self.board.push(move)
                    value = self.quiescence_search_max(alpha, beta, depth_left - 1)
                    mini = min(value, mini)
                    beta = min(beta, mini)
                    self.board.pop()
                    if mini <= alpha:
                        return mini
            return mini
        return self.evaluate_board(depth_left, len(moves))

    def quiescence_search_max(self, alpha, beta, depth_left):
        moves = self.board.generate_legal_moves()
        moves = list(moves)
        if depth_left > 0:
            self.visited_nodes += 1
            maxi = float('-inf')
            if not self.board.is_check():
                maxi = self.evaluate_board(depth_left, len(moves))
                if maxi >= beta:
                    return maxi
                alpha = max(alpha, maxi)
            n = self.board.legal_moves.count()
            if n == 0:
                if self.board.is_checkmate():
                    return -1000 * depth_left
                if self.board.is_stalemate():
                    return 0
            self.sort_moves(moves, self.player_colour)
            for move in moves:
                if self.board.gives_check(move) or self.board.is_capture(move) or self.board.is_check():
                    self.board.push(move)
                    value = self.quiescence_search_min(alpha, beta, depth_left - 1)
                    maxi = max(value, maxi)
                    alpha = max(alpha, maxi)
                    self.board.pop()
                    if maxi >= beta:
                        return maxi
            return maxi
        return self.evaluate_board(depth_left, len(moves))

    def print(self):
        print(self.board, end="\n --------------\n")
