import chess3 as ch

board = ch.Board()

def handle_move(from_coord, to_coord):
    try:
        # Преобразовать координаты в объект хода python-chess
        move = ch.Move.from_uci(f"{from_coord}{to_coord}")


        # Проверить, является ли ход легальным
        if move in board.legal_moves:
            board.push(move)  # Сделать ход на доске
            return {
                "move_made": True,
                "status": "success",
                "message": "Ход успешно выполнен"
            }
        else:
            return {
                "move_made": False,
                "status": "fail",
                "message": "Ход недопустим"
            }
    except ValueError:
        return {
            "move_made": False,
            "status": "error",
            "message": "Некорректный формат координат"
        }

class ChessLogic:
    def __init__(self):
        self.board = ch.Board()

    def is_valid_move(self, move):
        try:
            ch.Move.from_uci(move)
            return self.board.is_legal(move)
        except ValueError:
            return False

    def make_move(self, move):
        move = ch.Move.from_uci(move)
        if self.is_valid_move(move):
            self.board.push(move)
            return True
        return False
    def hangle_move(self):
        pass

    # Другие методы для управления игровой логикой...
