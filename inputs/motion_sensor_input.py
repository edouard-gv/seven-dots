import threading
from abc import ABC, abstractmethod
from gpiozero import MotionSensor
from inputs.video_input import VideoInput


class MotionSensor(VideoInput, ABC):
    def _wake_up(self, controller):
        controller.process_command("wake_up")

    @abstractmethod
    def start(self, controller):
        pass

    @abstractmethod
    def motion_detected(self):
        pass


class RaspiMotionSensor(MotionSensor):

    def __init__(self):
        self.pir = MotionSensor(4)

    def start(self, controller):
        if self.pir.motion_detected:
            self._wake_up(controller)
        else:
            self.pir.wait_for_motion()
            self._wake_up(controller)

    def motion_detected(self):
        return self.pir.motion_detected


class FakeMotionSensor(MotionSensor):

    def __init__(self):
        pass

    def fake_motion(self, controller):
        print("Fake motion detected")
        self._wake_up(controller)

    def start(self, controller):
        print("Fake motion sensor started")
        threading.Timer(2, lambda: self.fake_motion(controller)).start()

    def motion_detected(self):
        return False
