import statemachine

import classic_video_input
from display_computer import compute_display
from dots_machine import DotsMachine
from screen_output import MockSerialPort


class SevenDotsController:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.machine = None
        self.DISPLAY = [[0 for j in range(7)] for i in range(4)]

    def start(self):
        for output in self.outputs:
            output.start(self)
        self.machine = DotsMachine(self)
        for input in self.inputs:
            input.start(self)

    def process_command(self, gesture):
        try:
            self.machine.send(gesture.lower())
            # print("sending: "+gesture)
        except statemachine.exceptions.TransitionNotAllowed as tna:
            # print(str(tna))
            pass

    def process_state(self):
        compute_display(self.DISPLAY, self.machine)
        self.display()

    def display(self):
        for output in self.outputs:
            output.sendPrefix()
            for y in range(7):
                for x in range(4):
                    output.write(self.DISPLAY[x][y])
            output.sendClose()


if __name__ == '__main__':
    controller = SevenDotsController()
    controller.outputs.append(MockSerialPort())
    controller.inputs.append(classic_video_input.ClassicVideoInput())
    controller.start()
