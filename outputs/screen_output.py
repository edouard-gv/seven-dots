class ScreenPort:

    def start(self, controller):
        pass

    def send_bytes(self, *frame_bytes):
        for byte in frame_bytes:
            self.write(byte)

    def __init__(self) -> None:
        self.reset()
        self.output = ""

    def reset(self):
        self.in_header = True
        self.frame_bytes = []

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
            print(self.output)
            return
        self.frame_bytes.append(c)

    def compute_output(self):
        for p in range(4*7-len(self.frame_bytes)):
            self.frame_bytes.append(0)
        bytes_lines = [
            self.frame_bytes[i * 7: (i + 1) * 7] for i in range(4)
        ]

        lines_of_lines = []

        for byte_line in bytes_lines:
            converted_lines_to_transpose = [convert(b) for b in byte_line]
            converted_lines = [list(x) for x in list(zip(*converted_lines_to_transpose))]
            lines = [" ".join(line) + "\n" for line in converted_lines]
            lines_of_lines.append("".join(lines))

        blank_line = " " * (7 * 4 - 1) + "\n"
        self.output = blank_line.join(lines_of_lines)


def convert(c):
    return [
        " " + show_digit(c, 6, "_") + " ",
        show_digit(c, 1, "|") + show_digit(c, 0, "_") + show_digit(c, 5, "|"),
        show_digit(c, 2, "|") + show_digit(c, 3, "_") + show_digit(c, 4, "|"),
    ]


def show_digit(byte, bit, symbol):
    return symbol if byte & 2 ** bit else " "
