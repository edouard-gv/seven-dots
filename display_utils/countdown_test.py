import pytest

import display_utils.countdown
from display_utils.countdown import lit_countdown_position, countdown_position, hide_countdown_position, \
    highest_position_for_seconds


def test_18_should_lit_bottom_segment_of_l3c5_digit():
    display_matrix = [[0 for j in range(7)] for i in range(4)]
    lit_countdown_position(18, display_matrix)
    assert display_matrix[2][4] & 0b0001000 == 0b0001000


def test_18_should_hide_bottom_segment_of_l3c5_digit():
    display_matrix = [[0b1111111 for j in range(7)] for i in range(4)]
    hide_countdown_position(18, display_matrix)
    assert display_matrix[2][4] | 0b1110111 == 0b1110111


def test_18_position_should_be_4th_digit_on_l3c5():
    assert countdown_position(18) == (2, 4, 3)


def test_print_seconds_over60():
    assert display_utils.countdown.print_seconds(61) == " 1:01"


def test_print_seconds_under60():
    assert display_utils.countdown.print_seconds(9) == "   09"


@pytest.mark.parametrize("seconds, highest_position",
                         [(0, 0), (10, 10), (11, 11), (20, 11), (21, 12), (30, 12), (120, 21), (121, 22), (180, 22),
                          (240, 23), (300, 24), (600, 29)])
def test_highest_positions(seconds, highest_position):
    assert highest_position_for_seconds(seconds) == highest_position


def test_lit_all_positions_for_18pos():
    display_matrix = [[0 for j in range(7)] for i in range(4)]
    display_matrix = display_utils.countdown.lit_all_positions_for_seconds(85, display_matrix)
    assert display_matrix == [[0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 8, 8, 8, 0, 0],
                              [0, 73, 73, 73, 73, 73, 0]]
