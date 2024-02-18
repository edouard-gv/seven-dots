import time

from outputs.display import Display
from outputs.screen_output import ScreenPort


def countdown_position(param):
    if param > 30:
        return (0, 0, 0)
    map = [
        (3, 3, 3),  # 1
        (3, 2, 3),  # 2
        (3, 4, 3),  # 3
        (3, 3, 0),  # 4
        (3, 1, 3),  # 5
        (3, 5, 3),  # 6
        (3, 4, 0),  # 7
        (3, 2, 0),  # 8
        (3, 5, 0),  # 9
        (3, 1, 0),  # 10
        (3, 3, 6),  # 11
        (3, 2, 6),  # 12
        (3, 4, 6),  # 13
        (3, 1, 6),  # 14
        (3, 5, 6),  # 15
        (2, 3, 3),  # 16
        (2, 2, 3),  # 17
        (2, 4, 3),  # 18
        (2, 3, 0),  # 19
        (2, 4, 2),  # 20
        (2, 2, 4),  # 21
        (1, 3, 3),  # 22
        (1, 2, 3),  # 23
        (1, 4, 3),  # 24
        (1, 3, 4),  # 25
        (1, 3, 2),  # 26
        (1, 4, 2),  # 27
        (1, 2, 4),  # 28
        (1, 3, 0),  # 29
        (1, 3, 6),  # 30
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
        return (seconds-1) // 10 + 10
    else:
        return (seconds-1) // 60 + 20


def lit_all_positions_for_seconds(seconds, display_matrix):
    for n in range(1, seconds + 1):
        lit_countdown_position(highest_position_for_seconds(n), display_matrix)
    return display_matrix


if __name__ == "__main__":
    screen = ScreenPort()
    display = Display(screen)
    screen.start(None)
    matrix = [[0 for _ in range(7)] for _ in range(4)]
    for i in range(1, 31):
        print(f'Countdown: {i}')
        lit_countdown_position(i, matrix)
        display.update_display(matrix)


