import os

import numpy as np
from kernels.SSK import SSK

from .stringkernel import StringKernel


__author__ = 'Daniel Schlaug'

_dir = os.path.dirname(os.path.abspath(__file__))


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
        return SSK(self.__length, self.__weight_decay, string1, string2)

    def gram_matrix(self, row_arguments, column_arguments):
        path_prefix = os.path.join(_dir, "precomputed/done/SSK")
        testing_filename_flag = "-2"
        training_filename_flag = ""
        weight_decay_filename_prefix = "-lambda"
        length_filename_prefix = "-length"
        path_suffix = ".txt"
        length = self.__length
        weight_decay = self.__weight_decay
        if len(row_arguments) == len(column_arguments) == 380:
            path = path_prefix + training_filename_flag + length_filename_prefix + str(
                length) + weight_decay_filename_prefix + str(weight_decay) + path_suffix
            gram_matrix = self.__import_matrix(path)
        elif len(row_arguments) == 90 and len(column_arguments) == 380:
            path = path_prefix + testing_filename_flag + length_filename_prefix + str(
                length) + weight_decay_filename_prefix + str(weight_decay) + path_suffix
            gram_matrix = self.__import_matrix(path)
        elif len(row_arguments) == 380 and len(column_arguments) == 90:
            path = path_prefix + testing_filename_flag + length_filename_prefix + str(
                length) + weight_decay_filename_prefix + str(weight_decay) + path_suffix
            gram_matrix = self.__import_matrix(path).T
        else:
            raise Exception("Not implemented for non-precomputed matrices")
        return gram_matrix

    def __import_matrix(self, path):
        file = open(path)
        matrix = []
        row = []
        for line in file:
            try:
                value = float(line)
                row.append(value)
            except ValueError:
                matrix.append(row)
                row = []
        return np.matrix(matrix)