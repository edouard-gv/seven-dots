import alphabet


def test_print_text_with_no_pad():
    DISPLAY = [[0 for j in range(7)] for i in range(4)]
    alphabet.write("010", DISPLAY)
    assert DISPLAY == [
        [126, 48, 126, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]


def test_print_text_with_long_text():
    DISPLAY = [[0 for j in range(7)] for i in range(4)]
    alphabet.write("01010011000111000011110000011111", DISPLAY)
    assert DISPLAY == [
        [126, 48, 126, 48, 126, 126, 48],
        [48, 126, 126, 126, 48, 48, 48],
        [126, 126, 126, 126, 48, 48, 48],
        [48, 126, 126, 126, 126, 126, 48],
    ]


def test_print_text_with_pad():
    DISPLAY = [[0 for j in range(7)] for i in range(4)]
    alphabet.write("010", DISPLAY, line_shift=1, column_shift=1)
    print(DISPLAY)
    assert DISPLAY == [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 126, 48, 126, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]


def test_print_text_with_pad_return_line():
    DISPLAY = [[0 for j in range(7)] for i in range(4)]
    alphabet.write("0101010", DISPLAY, line_shift=1, column_shift=1)
    print(DISPLAY)
    assert DISPLAY == [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 126, 48, 126, 48, 126, 48],
        [126, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]


def test_print_extra_long_text_with_pad():
    DISPLAY = [[0 for j in range(7)] for i in range(4)]
    alphabet.write(
        "01010011000111000011110000011111", DISPLAY, line_shift=1, column_shift=1
    )
    print(DISPLAY)
    assert DISPLAY == [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 126, 48, 126, 48, 126, 126],
        [48, 48, 126, 126, 126, 48, 48],
        [48, 126, 126, 126, 126, 48, 48],
    ]


def test_print_dont_clear():
    DISPLAY = [[i * 7 + j for j in range(7)] for i in range(4)]
    alphabet.write("0101", DISPLAY, line_shift=1, column_shift=1)
    print(DISPLAY)
    assert DISPLAY == [
        [0, 1, 2, 3, 4, 5, 6],
        [7, 126, 48, 126, 48, 12, 13],
        [14, 15, 16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25, 26, 27],
    ]


def test_printseconds_over60():
    assert alphabet.print_seconds(61) == " 1:01"


def test_printseconds_under60():
    assert alphabet.print_seconds(9) == "   09"
