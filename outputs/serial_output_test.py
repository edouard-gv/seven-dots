from time import sleep

from outputs.display import Display
from outputs.serial_output import SerialPort

serial = SerialPort()
if serial.is_supported():
    disp = Display(serial)
    UW = 7
    UH = 4
    black = [[0b1111111 for _ in range(UW)] for _ in range(UH)]
    white = [[0 for _ in range(UW)] for _ in range(UH)]

    disp.start(None)
    disp.update_display(white)
    sleep(1)
    disp.update_display(black)
    sleep(1)
    disp.update_display(white)
    sleep(1)
    disp.update_display(black)
