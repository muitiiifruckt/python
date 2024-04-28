import unittest
from песочница import get_score # я использовал get_score в файле "песочница" учтите это

class TestGetScore(unittest.TestCase):

    def test_exact_offset(self):
        """Тестирование с точным совпадением offset"""
        game_stamps = [{"offset": 0, "score": {"home": 0, "away": 0}},
                       {"offset": 10, "score": {"home": 1, "away": 0}},
                       {"offset": 20, "score": {"home": 1, "away": 1}}]
        self.assertEqual(get_score(game_stamps, 10), (1, 0))

    def test_offset_between_stamps(self):
        """Тестирование с offset между существующими значениями"""
        game_stamps = [{"offset": 0, "score": {"home": 0, "away": 0}},
                       {"offset": 10, "score": {"home": 1, "away": 0}},
                       {"offset": 20, "score": {"home": 1, "away": 1}}]
        self.assertEqual(get_score(game_stamps, 15), (1, 0))

    def test_offset_below_first_stamp(self):
        """Тестирование с offset ниже первого значения"""
        game_stamps = [{"offset": 10, "score": {"home": 1, "away": 0}}]
        self.assertEqual(get_score(game_stamps, 5), (0, 0))

    def test_offset_above_last_stamp(self):
        """Тестирование с offset выше последнего значения"""
        game_stamps = [{"offset": 10, "score": {"home": 1, "away": 0}}]
        self.assertEqual(get_score(game_stamps, 20), (1, 0))

    def test_empty_game_stamps(self):
        """Тестирование пустого списка game_stamps"""
        game_stamps = []
        self.assertEqual(get_score(game_stamps, 10), (0, 0))

if __name__ == "__main__":
    unittest.main()
