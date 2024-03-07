from abc import ABCMeta, abstractmethod


class VideoInput(metaclass=ABCMeta):
    def __init__(self):
        self.force_stop = None

    @abstractmethod
    def start(self, controller):
        pass

    def stop(self):
        self.force_stop = True

