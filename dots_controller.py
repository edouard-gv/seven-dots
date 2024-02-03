from screen_output import MockSerialPort
import alphabet
from dots_machine import DotsMachine
import classic_video_input
import statemachine


class SevenDotsController:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.machine = None

    def start(self):
        for output in self.outputs:
            output.start(self)
        self.machine = DotsMachine(self)
        for input in self.inputs:
            input.start(self)

    def clear_display(self):
        self.DISPLAY = [[0 for j in range(7)] for i in range(4)]

    def fill_display(self):
        self.DISPLAY = [[0b1111111 for j in range(7)] for i in range(4)]

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
        if self.machine.current_state.name == "Black screen":
            self.fill_display()
        if self.machine.current_state.name == "Countdown confirm stop":
            alphabet.writeCenter("Stop ?", self.DISPLAY)
        if self.machine.current_state.name == "Countdown":
            if self.machine.countdown_running():
                alphabet.writeCenter(
                    alphabet.print_seconds(self.machine.countdown_value), self.DISPLAY
                )
        else:
            if self.machine.countdown_running() and not self.machine.current_state.name == "Bye":
                alphabet.write(
                    alphabet.print_seconds(self.machine.countdown_value), self.DISPLAY, line_shift=3
                )
        self.show()

    def show(self):
        for output in self.outputs:
            output.sendPrefix()
            for y in range(7):
                for x in range(4):
                    output.write(self.DISPLAY[x][y])
            output.sendClose()
            self.clear_display()


if __name__ == '__main__':
    controller = SevenDotsController()
    controller.outputs.append(MockSerialPort())
    controller.inputs.append(sevendots.ClassicVideoInput())
    controller.start()