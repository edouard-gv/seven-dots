import copy
from abc import ABCMeta, abstractmethod


class Port(metaclass=ABCMeta):
    @abstractmethod
    def start(self, controller):
        pass

    @abstractmethod
    def write(self, i):
        pass

    @abstractmethod
    def is_supported(self):
        pass


class Display:
    def __init__(self, output):
        self.UW = 7
        self.UH = 4
        self.display_matrix_copy = [[0 for _ in range(self.UW)] for _ in range(self.UH)]
        self.output = output

    def start(self, controller):
        self.output.start(controller)

    def update_display(self, display_matrix):
        if self.new_frame(display_matrix):
            self.output.write(0x80)
            self.output.write(0x83)
            self.output.write(0x00)

            for i in range(self.UH):
                for j in range(self.UW):
                    d = display_matrix[i][j]
                    self.output.write(d)

            self.output.write(0x8F)

        self.display_matrix_copy = copy.deepcopy(display_matrix)

    def new_frame(self, display_matrix):
        for j in range(self.UW):
            for i in range(self.UH):
                if display_matrix[i][j] != self.display_matrix_copy[i][j]:
                    return True
        return False
