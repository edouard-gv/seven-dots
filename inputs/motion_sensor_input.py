import threading
from abc import ABC, abstractmethod
from gpiozero import MotionSensor as MotionSensorGPIO
from inputs.video_input import VideoInput
from datetime import datetime
import logging

last_timestamp = datetime.now()

def compute_delta():
    global last_timestamp
    new_timestamp = datetime.now()
    delta = new_timestamp - last_timestamp
    last_timestamp = new_timestamp
    return delta

class MotionSensor(ABC):
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
        self.pir = MotionSensorGPIO(4)

    def start(self, controller):
        if self.pir.motion_detected:
            logging.getLogger("sevendots").warn("DEBUG EGV - should never happen: transition to standby should have been aborted")
            self._wake_up(controller)
        else:
            logging.getLogger("sevendots").debug(f'DEBUG EGV - entering standby mode after {compute_delta()}')
            self.pir.wait_for_motion()
            logging.getLogger("sevendots").debug(f'DEBUG EGV - exiting standby mode after {compute_delta()}')
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
