import threading
import time
from display_mock import MockSerialPort
import alphabet

screen = None
DISPLAY = []
current_gesture = None
frame = 0


def init():
    global DISPLAY
    DISPLAY = [[0 for j in range(7)] for i in range(4)]
    global screen
    screen = MockSerialPort()


def clear_display():
    global DISPLAY
    DISPLAY = [[0 for j in range(7)] for i in range(4)]


def clear_after(seconds, target_frame):
    global frame
    time.sleep(seconds)
    if frame == target_frame:
        clear_display()
        show(screen)


def process(gesture):
    global current_gesture
    if gesture == "Open_Palm" and current_gesture != "Open_Palm":
        current_gesture = "Open_Palm"
        alphabet.writeCenter("Salut", DISPLAY)
        show(screen)
    if gesture == "Closed_Fist" and current_gesture != "Closed_Fist":
        current_gesture = "Closed_Fist"
        alphabet.writeCenter("Bye", DISPLAY)
        show(screen)
        threading.Thread(target=clear_after, args=(2, frame)).start()


def show(screen):
    global frame
    frame += 1
    screen.sendPrefix()
    for y in range(7):
        for x in range(4):
            screen.write(DISPLAY[x][y])
    screen.sendClose()
    print(screen.output)
    clear_display()
