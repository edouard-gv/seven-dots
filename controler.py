from display_mock import MockSerialPort
import alphabet
from dots_machine import DotsMachine
import statemachine


class SevenDotsControler:
    def __init__(self):
        self.clear_display()
        self.machine = DotsMachine(self)
        self.screen = MockSerialPort()

    def clear_display(self):
        self.DISPLAY = [[0 for j in range(7)] for i in range(4)]

    def process(self, gesture):
        try:
            self.machine.send(gesture.lower())
            # print("sending: "+gesture)
        except statemachine.exceptions.TransitionNotAllowed as tna:
            # print(str(tna))
            pass

    def post_process(self):
        if self.machine.current_state.name == "Hello":
            alphabet.writeCenter("Salut", self.DISPLAY)
        if self.machine.current_state.name == "Bye":
            alphabet.writeCenter("Bye", self.DISPLAY)
        if self.machine.current_state.name == "Blank screen":
            self.clear_display()
        if self.machine.current_state.name == "Countdown confirm stop":
            alphabet.writeCenter("Stop ?", self.DISPLAY)
        if self.machine.current_state.name == "Countdown":
            if self.machine.countdown_running():
                alphabet.writeCenter(
                    str(int(self.machine.countdown_value)), self.DISPLAY
                )
        else:
            if self.machine.countdown_running():
                alphabet.write(
                    str(int(self.machine.countdown_value)), self.DISPLAY, line_shift=3
                )
        self.show()

    def show(self):
        self.screen.sendPrefix()
        for y in range(7):
            for x in range(4):
                self.screen.write(self.DISPLAY[x][y])
        self.screen.sendClose()
        self.clear_display()
