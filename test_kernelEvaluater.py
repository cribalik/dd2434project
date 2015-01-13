from unittest import TestCase

from kernelevaluater import KernelEvaluater
from kernels import SubSequenceStringKernel


__author__ = 'Daniel Schlaug'


class TestKernelEvaluater(TestCase):
    def test_evaluation(self):
        evaluater = KernelEvaluater(None, None, [SubSequenceStringKernel])

        evaluation = evaluater.evaluation({'length': 2, 'weight_decay': [4, 5, 6]})
        rows = evaluation.splitlines()
        self.failUnlessEqual(len(rows), 3)