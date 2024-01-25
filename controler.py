from display_mock import MockSerialPort
import alphabet

screen = None
DISPLAY = []


def init():
    global DISPLAY
    DISPLAY = [[0 for j in range(7)] for i in range(4)]
    global screen
    screen = MockSerialPort()


def clear_display():
    global DISPLAY
    DISPLAY = [[0 for j in range(7)] for i in range(4)]


def process(gesture):
    if gesture == "Open_Palm":
        alphabet.writeCenter("Salut", DISPLAY)
        show(screen)
    if gesture == "Closed_Fist":
        alphabet.writeCenter("Bye", DISPLAY)
        show(screen)


def show(screen):
    screen.sendPrefix()
    for y in range(7):
        for x in range(4):
            screen.write(DISPLAY[x][y])
    screen.sendClose()
    print(screen.output)
    clear_display()
