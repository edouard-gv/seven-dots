import copy

import statemachine

import classic_video_input
import raspi_video_input
from display_computer import compute_display
from dots_machine import DotsMachine
from screen_output import MockSerialPort
from serial_output import SerialPort

class Display:
    def __init__(self, output):
        self.UW = 7
        self.UH = 4
        self.DISPLAY_copy = [[0 for _ in range(self.UW)] for _ in range(self.UH)]
        self.output = output

    def start(self, controller):
        self.output.start(controller)

    def update_display(self, disp):
        if self.new_frame(disp):
            self.output.write(0x80)
            self.output.write(0x83)
            self.output.write(0x00)

            for i in range(self.UH):
                for j in range(self.UW):
                    d = disp[i][j]
                    self.output.write(d)

            self.output.write(0x8F)

        self.DISPLAY_copy = copy.deepcopy(disp)

    def new_frame(self, disp):
        for j in range(self.UW):
            for i in range(self.UH):
                if disp[i][j] != self.DISPLAY_copy[i][j]:
                    return True
        return False


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
        for disp in self.outputs:
            disp.update_display(self.DISPLAY)


if __name__ == '__main__':
    main_controller = SevenDotsController()
    main_controller.outputs.append(Display(MockSerialPort()))
    main_controller.outputs.append(Display(SerialPort()))
    # main_controller.inputs.append(classic_video_input.VideoInput())
    main_controller.inputs.append(raspi_video_input.VideoInput())
    main_controller.start()
