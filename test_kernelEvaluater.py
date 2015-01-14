from unittest import TestCase

import numpy

from kernelevaluater import KernelEvaluater, OutputFormat
from kernels import StringKernel
from kernels import NGramsStringKernel
from dataset import *
from reuters import Article


__author__ = 'Daniel Schlaug'

dummy_training_data = [
    Article(body="1", topics=["1"], data_type=DataType.training),
    Article(body="2", topics=["2"], data_type=DataType.training),
]

dummy_testing_data = [
    Article(body="1", topics=["1"], data_type=DataType.testing),
    Article(body="2", topics=["2"], data_type=DataType.testing),
]


class TestKernelEvaluater(TestCase):
    def test_evaluation(self):
        evaluater = KernelEvaluater(dummy_training_data, dummy_testing_data, [DummyKernel], topics=["1", "2"])

        latex_evaluation = evaluater.evaluation({'n':2, 'length': 2, 'weight_decay': [4, 5, 6]}, output_format=OutputFormat.latex)
        rows = latex_evaluation.splitlines()
        self.failUnlessEqual(len(rows), 7)

        python_evaluation = evaluater.evaluation({'n':[1, 2], 'length': 2, 'weight_decay': [4, 5, 6]}, output_format=OutputFormat.python)
        self.failUnlessEqual(len(python_evaluation), 12)

    # def test_real_data(self):
    #     dataset = Dataset()
    #     training_data = dataset.get_data(topic=None, data_type=DataType.training)
    #     test_data = dataset.get_data(topic=None, data_type=DataType.testing)
    #     evaluater = KernelEvaluater(training_data, test_data, kernels=[NGramsStringKernel], topics=[Topics.acquisition])
    #
    #     evaluation = evaluater.evaluation({'n': [3]})
    #     print(evaluation)
    #     rows = evaluation.splitlines()
    #     self.failUnlessEqual(len(rows), 1)


class DummyKernel(StringKernel):
    def __init__(self, **kwargs):
        pass

    def gram_matrix(self, row_arguments, column_arguments):
        return numpy.eye(N=len(row_arguments), M=len(column_arguments))

    def evaluate_for(self, string1, string2):
        return 1 if string1 == string2 else 0

    @staticmethod
    def name():
        return "Dummy Kernel"

    @staticmethod
    def understood_arguments():
        return ["n", "length", "weight_decay"]
