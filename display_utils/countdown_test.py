import pytest

import display_utils.countdown
from display_utils.countdown import lit_countdown_position, countdown_position, hide_countdown_position, \
    highest_position_for_seconds


def test_19_should_lit_upper_left_segment_of_l2c4_digit():
    display_matrix = [[0 for j in range(7)] for i in range(4)]
    lit_countdown_position(19,display_matrix)
    assert display_matrix[1][3] & 0b0100000 == 0b0100000


def test_19_should_hide_upper_left_segment_of_l2c4_digit():
    display_matrix = [[0b1111111 for j in range(7)] for i in range(4)]
    hide_countdown_position(19, display_matrix)
    assert display_matrix[1][3] | 0b1011111 == 0b1011111


def test_19_position_should_be_5th_digit_on_l2c4():
    assert countdown_position(19) == (1, 3, 5)


def test_print_seconds_over60():
    assert display_utils.countdown.print_seconds(61) == " 1:01"


def test_print_seconds_under60():
    assert display_utils.countdown.print_seconds(9) == "   09"


@pytest.mark.parametrize("seconds, highest_position",
                         [(0, 0), (10, 10), (11, 10), (19, 10), (20, 11), (29, 11), (119, 20), (120, 21), (180, 22),
                          (240, 23), (300, 24), (600, 29)])
def test_highest_positions(seconds, highest_position):
    assert highest_position_for_seconds(seconds) == highest_position


def test_lit_all_positions():
    display_matrix = [[0 for j in range(7)] for i in range(4)]
    display_matrix = display_utils.countdown.lit_all_positions(19, display_matrix)
    assert display_matrix == [[0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 24, 63, 12, 0, 0],
                              [0, 0, 96, 115, 66, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0]]
