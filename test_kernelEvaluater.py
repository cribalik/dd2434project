from unittest import TestCase
from tables import KernelEvaluater
from kernels import SubSequenceStringKernel

__author__ = 'Daniel Schlaug'


class TestKernelEvaluater(TestCase):
    def test_evaluation(self):
        evaluater = KernelEvaluater(None, None, [SubSequenceStringKernel])

        print(evaluater.evaluation({'length':2, 'gap_decay':[4,5,6]}))