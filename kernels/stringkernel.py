from abc import ABCMeta, abstractmethod

__author__ = 'Daniel Schlaug'


class StringKernel():
    __metaclass__ = ABCMeta
    """
    The base class for any string kernel to be used with the SVM.
    """

    @abstractmethod
    def evaluate_for(self, string1, string2):
        pass

    @abstractmethod
    def gram_matrix(self, row_arguments, column_arguments):
        pass

    @abstractmethod
    def name():
        """
        Static method returning a well formed name of the kernel for printing.
        :return: a well formed name of the kernel for printing.
        """
        pass

    @abstractmethod
    def understood_arguments():
        """
        Static method returning a list of strings containing the key-word arguments (kwargs) that the kernel's initializer understands.
        :return: a list of strings containing the key-word arguments (kwargs) that the kernel's initializer understands.
        """
        pass
