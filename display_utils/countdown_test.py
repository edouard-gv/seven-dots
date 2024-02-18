import pytest

import display_utils.countdown
from display_utils.countdown import lit_countdown_position, countdown_position, hide_countdown_position, \
    highest_position_for_seconds


def test_19_should_lit_upper_left_segment_of_l2c3_digit():
    display_matrix = [[0 for j in range(7)] for i in range(4)]
    lit_countdown_position(19, display_matrix)
    assert display_matrix[1][2] & 0b0100000 == 0b0100000


def test_19_should_hide_upper_left_segment_of_l2c3_digit():
    display_matrix = [[0b1111111 for j in range(7)] for i in range(4)]
    hide_countdown_position(19, display_matrix)
    assert display_matrix[1][2] | 0b1011111 == 0b1011111


def test_19_position_should_be_6th_digit_on_l2c3():
    assert countdown_position(19) == (1, 2, 5)


def test_print_seconds_over60():
    assert display_utils.countdown.print_seconds(61) == " 1:01"


def test_print_seconds_under60():
    assert display_utils.countdown.print_seconds(9) == "   09"


@pytest.mark.parametrize("seconds, highest_position",
                         [(0, 0), (10, 10), (11, 11), (20, 11), (21, 12), (30, 12), (120, 21), (121, 22), (180, 22),
                          (240, 23), (300, 24), (600, 29)])
def test_highest_positions(seconds, highest_position):
    assert highest_position_for_seconds(seconds) == highest_position


def test_lit_all_positions_for_19pos():
    display_matrix = [[0 for j in range(7)] for i in range(4)]
    display_matrix = display_utils.countdown.lit_all_positions_for_seconds(95, display_matrix)
    assert display_matrix == [[0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 104, 28, 74, 0, 0],
                              [0, 0, 88, 106, 76, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0]]
