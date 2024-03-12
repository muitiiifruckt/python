from pprint import pprint
import random
import math

TIMESTAMPS_COUNT = 50000

PROBABILITY_SCORE_CHANGED = 0.0001

PROBABILITY_HOME_SCORE = 0.45

OFFSET_MAX_STEP = 3

INITIAL_STAMP = {
    "offset": 0,
    "score": {
        "home": 0,
        "away": 0
    }
}


def generate_stamp(previous_value):
    score_changed = random.random() > 1 - PROBABILITY_SCORE_CHANGED
    home_score_change = 1 if score_changed and random.random() > 1 - \
        PROBABILITY_HOME_SCORE else 0
    away_score_change = 1 if score_changed and not home_score_change else 0
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    return {
        "offset": previous_value["offset"] + offset_change,
        "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change
        }
    }


def generate_game():
    stamps = [INITIAL_STAMP, ]
    current_stamp = INITIAL_STAMP
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps

def get_score(game_stamps, offset):
    left, right = 0, len(game_stamps) - 1
    while left <= right:
        mid = (left + right) // 2
        if game_stamps[mid]["offset"] == offset:
            return game_stamps[mid]["score"]["home"], game_stamps[mid]["score"]["away"]
        elif game_stamps[mid]["offset"] < offset:
            left = mid + 1
        else:
            right = mid - 1

    # На этом этапе right указывает на наибольший индекс, чей offset меньше или равен искомому.
    # Это условие нужно для корректной работы, даже если точный offset не найден.
    if right >= 0:
        return game_stamps[right]["score"]["home"], game_stamps[right]["score"]["away"]
    else:
        # Если искомый offset меньше первого offset в game_stamps, вернуть начальный счет.
        return (INITIAL_STAMP["score"]["home"],INITIAL_STAMP["score"]["home"])

game_stamps = generate_game()

pprint(game_stamps)
pprint(get_score(game_stamps,-10))


