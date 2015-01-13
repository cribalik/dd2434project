from .stringkernel import StringKernel

__author__ = 'Daniel Schlaug'


class SubSequenceStringKernel(StringKernel):
    def __init__(self, length, gap_decay):
        self.__length = length
        self.__gap_decay = gap_decay

    @staticmethod
    def name():
        return "Sub-Sequence"

    @staticmethod
    def understood_arguments():
        return ["length", "gap_decay"]

    def evaluate_for(self, string1, string2):
        pass