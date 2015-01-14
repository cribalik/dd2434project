from unittest import TestCase
from kernels import SubSequenceStringKernel

from numpy import zeros, shape

__author__ = 'Daniel Schlaug'


class TestSubSequenceStringKernelIT(TestCase):
    def test_hard_coded_gram_matrix(self):
        lengths = [3, 4, 5, 6, 7, 8, 10, 12, 14]
        weight_decays = [0.01, 0.03, 0.05, 0.07, 0.09, 0.1, 0.3, 0.5, 0.7, .9]
        for length in lengths:
            ssk = SubSequenceStringKernel(length, 0.5)
            gram_matrix = ssk.gram_matrix(zeros(380), zeros(380))
            self.failUnless(shape(gram_matrix) == (380, 380), "Failed for length %i. Actual shape = %s" % (length, str(shape(gram_matrix))))
            gram_matrix_testing = ssk.gram_matrix(zeros(90), zeros(380))
            self.failUnless(shape(gram_matrix_testing) == (90, 380), "Failed for length %i. Actual shape = %s" % (length, str(shape(gram_matrix_testing))))
        for weight_decay in weight_decays:
            ssk = SubSequenceStringKernel(5, weight_decay)
            gram_matrix = ssk.gram_matrix(zeros(380), zeros(380))
            self.failUnless(shape(gram_matrix) == (380, 380), "Failed for weight decay %i. Actual shape = %s" % (weight_decay, str(shape(gram_matrix))))
            gram_matrix_testing = ssk.gram_matrix(zeros(90), zeros(380))
            self.failUnless(shape(gram_matrix_testing) == (90, 380), "Failed for weight decay %i. Actual shape = %s" % (weight_decay, str(shape(gram_matrix_testing))))