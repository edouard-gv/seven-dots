class MockSerialPort:

    def start(self, controller):
        pass

    def sendPrefix(self):
        self.write(0x80)
        self.write(0x83)
        self.write(0x00)

    def sendClose(self):
        self.write(0x8F)
        print(self.output)

    def sendBytes(self, *bytes):
        for byte in bytes:
            self.write(byte)

    def __init__(self) -> None:
        self.reset()
        self.output = ""

    def reset(self):
        self.line_nb = 0
        self.lines = []
        self.in_header = True
        for i in range(4):
            self.lines += [[[], [], []]]

    def write(self, c):
        if c == 0x80:
            self.reset()
            return
        if self.in_header:
            if c == 0x83:
                return
            if c == 0x00:
                self.in_header = False
                return
        if c == 0x8F:
            self.compute_output()
            return
        convertion = convert(c)
        for subline_nb in range(3):
            self.lines[self.line_nb][subline_nb] += [convertion[subline_nb]]
        self.line_nb = (self.line_nb + 1) % 4

    def compute_output(self):
        def structured_to_string(structured_fragment):
            return " ".join(structured_fragment).ljust(7 * 4 - 1) + "\n"

        subline_string_list = []

        empty_line = " " * (7 * 4 - 1) + "\n"

        for line in self.lines:
            subline_string_list += [
                "".join(
                    [
                        structured_to_string(structured_subline)
                        for structured_subline in line
                    ]
                )
            ]

        self.output = empty_line.join(subline_string_list)


def convert(c):
    return [
        " " + show_digit(c, 6, "_") + " ",
        show_digit(c, 1, "|") + show_digit(c, 0, "_") + show_digit(c, 5, "|"),
        show_digit(c, 2, "|") + show_digit(c, 3, "_") + show_digit(c, 4, "|"),
    ]


def show_digit(byte, bit, symbol):
    return symbol if byte & 2 ** bit else " "
