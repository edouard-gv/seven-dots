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

    def clear_screen(self):
        self.clear_display()
        self.show()

    def process(self, gesture):
        try:
            self.machine.send(gesture.lower())
            #print("sending: "+gesture)
        except statemachine.exceptions.TransitionNotAllowed as tna:
            #print(str(tna))
            pass

    def post_process(self):
        if self.machine.current_state.name == "Hello":
            alphabet.writeCenter("Salut", self.DISPLAY)
            self.show()
        if self.machine.current_state.name == "Bye":
            alphabet.writeCenter("Bye", self.DISPLAY)
            self.show()
        if self.machine.current_state.name == "Blank screen":
            self.clear_screen()

    def show(self):
        self.screen.sendPrefix()
        for y in range(7):
            for x in range(4):
                self.screen.write(self.DISPLAY[x][y])
        self.screen.sendClose()
        self.clear_display()
