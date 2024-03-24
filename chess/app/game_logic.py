import chess


def handle_move(from_coord, to_coord):
    return {
        "move_made": True,
        "status": "success",
        "message": "Ход успешно выполнен"
    }
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
    def hangle_move(self):
        pass

    # Другие методы для управления игровой логикой...
