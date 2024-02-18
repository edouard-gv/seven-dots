import os
from abc import ABCMeta, abstractmethod

from dots_machine import DotsMachine


class SystemControl(metaclass=ABCMeta):
    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def update(self):
        pass

    def process_system_state(self, machine: DotsMachine):
        if machine.is_system_state():
            if machine.current_state.value == "system_shutdown":
                self.shutdown()
            elif machine.current_state.value == "system_update":
                self.update()


class LinuxSystemControl(SystemControl):
    def shutdown(self):
        os.system("sudo systemctl poweroff")

    def update(self):
        os.system("bash /home/pi/seven-dots/update.sh")


class FakeSystemControl(SystemControl):
    def __init__(self):
        self.shutdown_called = False
        self.update_called = False

    def shutdown(self):
        self.shutdown_called = True
        print("fake shutdown now :)")

    def is_shutdown(self):
        return self.shutdown_called

    def update(self):
        self.update_called = True
        print("fake update now :)")

    def is_update(self):
        return self.update_called
