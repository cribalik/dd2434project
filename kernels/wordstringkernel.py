# coding=utf-8
from dataset import Dataset
from kernels import StringKernel
from kernels import wk, gram
from reuters import DataType

__author__ = 'David Strömberg'


class WordStringKernel(StringKernel):
    
    def __init__(self):
        self.__idf_cached = None

    @property
    def __idf(self):
        if self.__idf_cached is None:
            dataset = Dataset()
            docs = dataset.get_data(topic=None, data_type=DataType.training) + \
                   dataset.get_data(topic=None, data_type=DataType.testing)
            docs = [article.body for article in docs]
            self.__idf_cached = wk.get_idf(docs)
        return self.__idf_cached


    def gram_matrix(self, row_arguments, column_arguments):
        return gram.gram(column_arguments, row_arguments, wk.wk(self.__idf))


    def evaluate_for(self, string1, string2):
        return wk.wkkernel(string1, string2, self.__idf)

    @staticmethod
    def name():
        return 'Word Kernel (WK)'

    @staticmethod
    def understood_arguments():
        return []