import os
import threading

import statemachine

from ext_openmeteo.openmeteo import OpenMeteo
from inputs.classic_video_input import ClassicVideoInput
from inputs.motion_sensor_input import RaspiMotionSensor, FakeMotionSensor, MotionSensor
from inputs.raspi_video_input import RaspiVideoInput
from inputs.video_input import VideoInput
from display_computer import compute_display
from dots_machine import DotsMachine
from outputs.display import Port, Display
from outputs.screen_output import ScreenPort
from outputs.serial_output import SerialPort
from system_control import SystemControl, LinuxSystemControl, FakeSystemControl


class SevenDotsController:
    def __init__(self):
        self.sensor: MotionSensor = select_motion_sensor()
        self.input: VideoInput = select_video_input()
        self.outputs: list[Display] = []
        self.machine: DotsMachine = None
        self.system_control: SystemControl = FakeSystemControl() if os.name == 'nt' else LinuxSystemControl()
        self.open_meteo = OpenMeteo()

    def start(self):
        for output in self.outputs:
            output.start(self)
        self.machine = DotsMachine(self)
        self.process_command("init")
        self.input.start(self)

    def append_display_from_output(self, output: Port):
        if output.is_supported():
            print("Adding display"+str(output))
            self.outputs.append(Display(output))

    def process_command(self, gesture):
        if gesture == "wake_up":
            try:
                self.machine.send(gesture.lower())
            except statemachine.exceptions.TransitionNotAllowed as tna:
                # print(f"Exception in {self.machine.__class__} '{self.__hash__()}: {tna}")
                pass
            threading.Timer(0, self.input.start(self)).start()
        else:
            try:
                self.machine.send(gesture.lower())
            except statemachine.exceptions.TransitionNotAllowed as tna:
                # print(f"Exception in {self.machine.__class__} '{self.__hash__()}: {tna}")
                pass

    def process_state(self):
        display_matrix = compute_display(self.machine)
        for disp in self.outputs:
            disp.update_display(display_matrix)
        if self.machine.is_system_state():
            self.system_control.process_system_state(self.machine)
        if self.machine.current_state == self.machine.standby_screen:
            threading.Timer(0, self.sensor.start(self)).start()
            self.input.stop()


def select_video_input():
    return ClassicVideoInput() if os.name == 'nt' else RaspiVideoInput()


def select_motion_sensor():
    return FakeMotionSensor() if os.name == 'nt' else RaspiMotionSensor()


if __name__ == '__main__':
    main_controller = SevenDotsController()
    main_controller.append_display_from_output(ScreenPort())
    main_controller.append_display_from_output(SerialPort())
    main_controller.start()
