import statemachine

from inputs.video_input import VideoInput
from inputs.classic_video_input import ClassicVideoInput
from inputs.raspi_video_input import RaspiVideoInput
from display_computer import compute_display
from dots_machine import DotsMachine
from outputs.display import Port, Display
from outputs.screen_output import ScreenPort
from outputs.serial_output import SerialPort


class SevenDotsController:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.machine = None

    def start(self):
        for output in self.outputs:
            output.start(self)
        self.machine = DotsMachine(self)
        self.process_command("init")
        for input in self.inputs:
            input.start(self)

    def append_input(self, video_input: VideoInput):
        if video_input.is_supported():
            print("Adding input"+str(video_input))
            self.inputs.append(video_input)

    def append_display_from_output(self, output: Port):
        if output.is_supported():
            print("Adding display"+str(output))
            self.outputs.append(Display(output))

    def process_command(self, gesture):
        try:
            self.machine.send(gesture.lower())
        except statemachine.exceptions.TransitionNotAllowed as tna:
            pass

    def process_state(self):
        display_matrix = compute_display(self.machine)
        for disp in self.outputs:
            disp.update_display(display_matrix)


if __name__ == '__main__':
    main_controller = SevenDotsController()
    main_controller.append_display_from_output(ScreenPort())
    main_controller.append_display_from_output(SerialPort())
    main_controller.append_input(ClassicVideoInput())
    main_controller.append_input(RaspiVideoInput())
    main_controller.start()
