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
    def understood_arguments():
        pass

    @abstractmethod
    def name():
        pass