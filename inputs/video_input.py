from abc import ABCMeta, abstractmethod


class VideoInput(metaclass=ABCMeta):
    @abstractmethod
    def start(self, controller):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def is_supported(self):
        pass
