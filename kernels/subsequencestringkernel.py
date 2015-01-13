from .stringkernel import StringKernel
import numpy as np

__author__ = 'Daniel Schlaug'


class SubSequenceStringKernel(StringKernel):
    def __init__(self, length, weight_decay):
        self.__length = length
        self.__weight_decay = weight_decay

    @staticmethod
    def name():
        return "Sub-Sequence"

    @staticmethod
    def understood_arguments():
        return ["length", "weight_decay"]

    def evaluate_for(self, string1, string2):
        pass

    def gram_matrix(self, row_arguments, column_arguments):
        base_filename
        if len(row_arguments) == len(column_arguments) == 380:
            length = self.__length
            weight_decay = self.__weight_decay
            numpy.loadtxt(open("test.csv","rb"),delimiter=",",skiprows=1)
        elif len(row_arguments) == 90 and len(column_arguments) == 380:

        elif len(row_arguments) == 380 and len(column_arguments) == 90:

            return gram_matrix.T