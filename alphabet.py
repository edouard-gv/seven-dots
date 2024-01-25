alphabet = " 0123456789-abcdefghijklmnopqrstuvwxyz"
alphabet_bin = [
        0b0000000, # spacja
        0b1111110, # 0
        0b0110000, # 1
        0b1101101, # 2
        0b1111001, # 3
        0b0110011, # 4
        0b1011011, # 5
        0b1011111, # 6
        0b1110000, # 7
        0b1111111, # 8
        0b1111011, # 9

        0b0000001, # -

        0b1110111, # a
        0b1111111, # b
        0b1001110, # c
        0b0111101, # d
        0b1001111, # e
        0b1000111, # f
        0b1011110, # g
        0b0110111, # h
        0b0110000, # i
        0b1111100, # j
        0b1010111, # k - bad
        0b0001110, # l
        0b1110110, # m
        0b0010101, # n
        0b1111110, # o
        0b1100111, # p
        0b1110011, # q
        0b1000110, # r
        0b1011011, # s
        0b1110000, # t - bad
        0b0111110, # u
        0b0100111, # v - bad
        0b0110110, # w - bad
        0b0010011, # x - bad
        0b0111011, # y
        0b1101101, # z
    ]

nums = [
    0b1111110, # 0
    0b0110000, # 1
    0b1101101, # 2
    0b1111001, # 3
    0b0110011, # 4
    0b1011011, # 5
    0b1011111, # 6
    0b1110000, # 7
    0b1111111, # 8
    0b1111011  # 9
    ] 

def write(text, DISPLAY):
  text = text.lower()
  strLen = min(len(text), 7*4)
  for pos in range(strLen):
    ind = alphabet.find(text[pos])
    y = pos % 7
    x = pos // 7
    if ind >= 0:
      DISPLAY[x][y] = alphabet_bin[ind]

def writeCenter(text, DISPLAY):
  spaces = ""
  spacesLength = (7//2-1)*7 + (7-len(text))//2
  for i in range(spacesLength):
    spaces += " "
  write(spaces+text, DISPLAY)
