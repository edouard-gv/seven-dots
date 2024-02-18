import time

from outputs.display import Display
from outputs.screen_output import ScreenPort


def countdown_position(param):
    if param > 30:
        return (0, 0, 0)
    map = [
        (1, 3, 3),  # 1
        (2, 3, 6),  # 2
        (2, 3, 1),  # 3
        (1, 3, 4),  # 4
        (2, 3, 5),  # 5
        (1, 3, 2),  # 6
        (1, 2, 3),  # 7
        (2, 2, 6),  # 8
        (2, 4, 6),  # 9
        (1, 4, 3),  # 10
        (1, 4, 2),  # 11
        (2, 2, 5),  # 12
        (2, 4, 1),  # 13
        (1, 2, 4),  # 14
        (1, 3, 0),  # 15
        (2, 3, 0),  # 16
        (1, 3, 1),  # 17
        (2, 3, 4),  # 18
        (1, 3, 5),  # 19
        (2, 3, 2),  # 20
        (1, 3, 6),  # 21
        (2, 3, 3),  # 22
        (1, 2, 0),  # 23
        (2, 4, 0),  # 24
        (2, 2, 0),  # 25
        (1, 4, 0),  # 26
        (1, 4, 1),  # 27
        (2, 2, 4),  # 28
        (1, 2, 5),  # 29
        (2, 4, 2),  # 30
    ]

    return map[param - 1]


def lit_countdown_position(number, display_matrix):
    (i, j, p) = countdown_position(number)
    display_matrix[i][j] |= 2 ** p


def hide_countdown_position(number, display_matrix):
    (i, j, p) = countdown_position(number)
    display_matrix[i][j] &= 0b1111111 - 2 ** p


# converting seconds to time
def print_seconds(seconds):
    minutes = seconds // 60
    seconds %= 60
    return f"{minutes:>2}:{seconds:02}" if minutes else f"   {seconds:02}"


def highest_position_for_seconds(seconds):
    if seconds <= 10:
        return seconds
    if seconds <= 120:
        return seconds // 10 + 9
    else:
        return seconds // 60 + 19


def lit_all_positions(seconds, display_matrix):
    for n in range(1, seconds + 1):
        lit_countdown_position(highest_position_for_seconds(n), display_matrix)
    return display_matrix
