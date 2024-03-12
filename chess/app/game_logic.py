import chess


class ChessLogic:
    def __init__(self):
        self.board = chess.Board()

    def is_valid_move(self, move):
        try:
            chess.Move.from_uci(move)
            return self.board.is_legal(move)
        except ValueError:
            return False

    def make_move(self, move):
        move = chess.Move.from_uci(move)
        if self.is_valid_move(move):
            self.board.push(move)
            return True
        return False

    # Другие методы для управления игровой логикой...
