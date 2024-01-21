import copy

class Display:
    def __init__(self):
        self.UW = 7
        self.UH = 4
        self.DISPLAY = [[0 for _ in range(self.UH)] for _ in range(self.UW)]
        self.DISPLAY_copy = copy.deepcopy(self.DISPLAY)
        self.senddataOn = True
        self.mySerialPort = SerialPort()

    def update_display(self):
        if self.new_frame() and self.senddataOn:
            self.mySerialPort.write(0x80)
            self.mySerialPort.write(0x83)
            self.mySerialPort.write(0x00)

            for y in range(self.UH):
                for x in range(self.UW):
                    d = self.DISPLAY[x][y]
                    self.mySerialPort.write(d)

            self.mySerialPort.write(0x8F)

        self.DISPLAY_copy = copy.deepcopy(self.DISPLAY)

    def new_frame(self):
        for x in range(self.UW):
            for y in range(self.UH):
                if self.DISPLAY[x][y] != self.DISPLAY_copy[x][y]:
                    return True
        return False

class SerialPort:
    def __init__(port = 0):
        pass

    def write(self, i):
        print(i)

