import serial


class SerialPort:
    def __init__(self):
        self.ser = None

    def start(self, controller):
        self.ser = serial.Serial('/dev/serial0')
        self.ser.baudrate = 57600
        print(self.ser)

    def write(self, i):
        self.ser.write(bytes([i]))
