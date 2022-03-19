from chess import Board
import chess as c


def evaluate(board: Board, colour: bool):
    white = 0
    black = 0
    symbols = ['Q', 'R', 'N', 'B', 'P']
    values = [9, 5, 3, 3, 1]
    for i in range(len(symbols)):
        white += len(board.pieces(c.Piece.from_symbol(symbols[i]).piece_type, True))*values[i]
        black += len(board.pieces(c.Piece.from_symbol(symbols[i]).piece_type, False))*values[i]
    if colour:
        return white - black
    return black - white


def min_(board: Board, colour: bool, depth_left: int):
    if depth_left > 0:
        n = board.legal_moves.count()
        if n == 0:
            if board.is_checkmate():
                return float('-inf')
        D = [float('inf') for _ in range(n)]
        moves = board.generate_legal_moves()
        for i in range(n):
            move = next(moves)
            board.push(move)
            D[i] = max_(board, colour, depth_left - 1)
            board.pop()
        return min(D)
    return evaluate(board, colour)


def max_(board: Board, colour: bool, depth_left: int):
    if depth_left > 0:
        n = board.legal_moves.count()
        if n == 0:
            if board.is_checkmate():
                return float('inf')
        D = [float('inf') for _ in range(n)]
        moves = board.generate_legal_moves()
        for i in range(n):
            move = next(moves)
            board.push(move)
            D[i] = min_(board, colour, depth_left - 1)
            board.pop()
        return max(D)
    return evaluate(board, colour)


def calculate_move(board: Board, colour: bool, depth_left: int):
    n = board.legal_moves.count()
    D = [[float('-inf'), None] for _ in range(n)]
    moves = board.generate_legal_moves()
    for i in range(n):
        move = next(moves)
        board.push(move)
        D[i][0] = min_(board, colour, depth_left - 1)
        D[i][1] = move
        board.pop()
    best_value = float('-inf')
    best_valued_move = None
    for i in range(n):
        if D[i][0] > best_value:
            best_value = D[i][0]
            best_valued_move = D[i][1]
    return best_valued_move


board = Board()
for i in range(10):
    white_move = calculate_move(board, True, 3)
    board.push(white_move)
    print(board)
    print("value", evaluate(board, True))
    print("white")
    print("-----------------------")
    black_move = calculate_move(board, False, 3)
    board.push(black_move)
    print(board)
    print("value", evaluate(board, False))
    print("black")
    print("-----------------------")
