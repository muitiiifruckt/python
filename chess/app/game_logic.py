import chess3 as ch

board = ch.Board()

def handle_move(from_coord, to_coord, promo=None):
    try:
        # Преобразовать координаты в объект хода python-chess
        move_uci = f"{from_coord}{to_coord}"
        if promo:
            move_uci += promo  # Добавляем символ превращения к UCI хода, если он есть
        print(promo)
        print(move_uci)
        move = ch.Move.from_uci(move_uci)        # Проверить, является ли ход легальным
        print(move)
        if move in board.legal_moves:
            en_passant_move = board.is_en_passant(move)
            board.push(move)  # Сделать ход на доске
            chekmate = board.is_checkmate()
            stalemate = board.is_stalemate()
            is_insufficient_material = board.is_insufficient_material()

            return {
                "move_made": True,
                "status": "success",
                "chekmate": chekmate,
                "stalemate": stalemate,
                "is_insufficient_material":is_insufficient_material,
                "en_passant_move": en_passant_move,
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
