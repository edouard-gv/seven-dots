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
        (2, 4, 2),  # 11
        (2, 2, 4),  # 12
        (2, 4, 3),  # 13
        (2, 2, 3),  # 14
        (2, 3, 3),  # 15
        (1, 4, 6),  # 16
        (1, 2, 6),  # 17
        (1, 4, 1),  # 18
        (1, 2, 5),  # 19
        (1, 3, 5),  # 20
        (1, 3, 1),  # 21
        (0, 4, 3),  # 22
        (0, 2, 3),  # 23
        (0, 4, 2),  # 24
        (0, 2, 4),  # 25
        (0, 3, 4),  # 26
        (0, 3, 2),  # 27
        (0, 3, 5),  # 28
        (0, 3, 1),  # 29
        (0, 3, 6),  # 30
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


