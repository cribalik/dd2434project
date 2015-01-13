# coding=utf-8
from kernels import StringKernel

__author__ = 'David Strömberg'


class WordStringKernel(StringKernel):
    def __init__(self):
        # Calculate idf and stuff using Pontus' functions.
        pass

    def gram_matrix(self, row_arguments, column_arguments):
        pass

    def evaluate_for(self, string1, string2):
        pass

    @staticmethod
    def name():
        # This name will show in our tables
        pass

    @staticmethod
    def understood_arguments():
        # A string containing the exact arguments of __init__()
        pass
