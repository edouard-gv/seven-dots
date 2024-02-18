from display_utils import alphabet


def test_print_text_with_no_pad():
    display = [[0 for j in range(7)] for i in range(4)]
    alphabet.write("010", display)
    assert display == [
        [126, 48, 126, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]


def test_print_text_with_long_text():
    display = [[0 for j in range(7)] for i in range(4)]
    alphabet.write("01010011000111000011110000011111", display)
    assert display == [
        [126, 48, 126, 48, 126, 126, 48],
        [48, 126, 126, 126, 48, 48, 48],
        [126, 126, 126, 126, 48, 48, 48],
        [48, 126, 126, 126, 126, 126, 48],
    ]


def test_print_text_with_pad():
    display = [[0 for j in range(7)] for i in range(4)]
    alphabet.write("010", display, line_shift=1, column_shift=1)
    print(display)
    assert display == [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 126, 48, 126, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]


def test_print_text_with_pad_return_line():
    display = [[0 for j in range(7)] for i in range(4)]
    alphabet.write("0101010", display, line_shift=1, column_shift=1)
    print(display)
    assert display == [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 126, 48, 126, 48, 126, 48],
        [126, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]


def test_print_extra_long_text_with_pad():
    display = [[0 for j in range(7)] for i in range(4)]
    alphabet.write(
        "01010011000111000011110000011111", display, line_shift=1, column_shift=1
    )
    print(display)
    assert display == [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 126, 48, 126, 48, 126, 126],
        [48, 48, 126, 126, 126, 48, 48],
        [48, 126, 126, 126, 126, 48, 48],
    ]


def test_print_dont_clear():
    display = [[i * 7 + j for j in range(7)] for i in range(4)]
    alphabet.write("0101", display, line_shift=1, column_shift=1)
    print(display)
    assert display == [
        [0, 1, 2, 3, 4, 5, 6],
        [7, 126, 48, 126, 48, 12, 13],
        [14, 15, 16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25, 26, 27],
    ]