from kernels import StringKernel
from kernels import ngk
from kernels import gram

__author__ = 'Eric Hörberg'

class NGramsStringKernel(StringKernel):
    def __init__(self, n):
        self.n = n

    def gram_matrix(self, row_arguments, column_arguments):
        gram.gram(column_arguments, row_arguments, ngk.ngk(self.n))
        pass

    def evaluate_for(self, string1, string2):
        return ngk.ngkernel(string1, string2, self.n)

    @staticmethod
    def name():
        return "n-grams kernel"

    @staticmethod
    def understood_arguments():
        return ['n']