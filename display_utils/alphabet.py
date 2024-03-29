alphabet = " 0123456789-abcdefghijklmnopqrstuvwxyz?':.+_"
alphabet_bin = [
    0b0000000,  # spacja
    0b1111110,  # 0
    0b0110000,  # 1
    0b1101101,  # 2
    0b1111001,  # 3
    0b0110011,  # 4
    0b1011011,  # 5
    0b1011111,  # 6
    0b1110000,  # 7
    0b1111111,  # 8
    0b1111011,  # 9
    0b0000001,  # -
    0b1110111,  # a
    0b0011111,  # b
    0b1001110,  # c
    0b0111101,  # d
    0b1001111,  # e
    0b1000111,  # f
    0b1011110,  # g
    0b0110111,  # h
    0b0110000,  # i
    0b1111100,  # j
    0b1010111,  # k - bad
    0b0001110,  # l
    0b1110110,  # m
    0b0010101,  # n
    0b1111110,  # o
    0b1100111,  # p
    0b1110011,  # q
    0b0000101,  # r
    0b1011011,  # s
    0b1110000,  # t - bad
    0b0111110,  # u
    0b0100111,  # v - bad
    0b0110110,  # w - bad
    0b0010011,  # x - bad
    0b0111011,  # y
    0b1101101,  # z
    0b1100100,  # ?
    0b0000010,  # '
    0b0001001,  # :
    0b0000100,  # .
    0b0000101,  # + - bad
    0b0001000,  # _
]

nums = [
    0b1111110,  # 0
    0b0110000,  # 1
    0b1101101,  # 2
    0b1111001,  # 3
    0b0110011,  # 4
    0b1011011,  # 5
    0b1011111,  # 6
    0b1110000,  # 7
    0b1111111,  # 8
    0b1111011,  # 9
]


def write(text, display_matrix, line_shift=0, column_shift=0):
    pad = line_shift * 7 + column_shift
    text = text.lower()
    strLen = min(len(text), 7 * 4 - pad)
    for pos in range(strLen):
        ind = alphabet.find(text[pos])
        y = (pos + pad) % 7
        x = (pos + pad) // 7
        if ind >= 0:
            display_matrix[x][y] = alphabet_bin[ind]


def center_in_screen(text, display_matrix):
    spaces = ""
    spacesLength = 7 + (7 - len(text)) // 2
    for i in range(spacesLength):
        spaces += " "
    write(spaces + text, display_matrix)


def center_in_line(text, display_matrix, line):
    write(text, display_matrix, line_shift=line, column_shift=(7 - len(text)) // 2)


def generate_bytes_string(text):
    return "".join(['\\x{0:02x}'.format(alphabet_bin[alphabet.find(char)]) for char in text.lower()])
