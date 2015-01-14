from enum import Enum
from sklearn import svm

from confusionmatrix import ConfusionMatrix
from dataset import Topics

from kernels import NGramsStringKernel

import numpy as np

__author__ = 'Daniel Schlaug'


class OutputFormat(Enum):
    latex = 'LaTeX'


class KernelEvaluater:
    def __init__(self, training_data, test_data, kernels, topics=Topics):
        self.training_data = training_data
        self.test_data = test_data
        self.kernels = kernels
        self.topics = topics

    def __kernel_arg_name(self, kwargs):
        kernel_arg_name = self.varying_kernel_args.keys()[0]
        kernel_arg_name = kernel_arg_name.replace('_', ' ').capitalize()
        return kernel_arg_name

    def confusion_matrix(self, kernel, kernel_kwargs, topic):
        kernel = kernel(**kernel_kwargs)
        test_bodies = [article.body for article in self.test_data]
        training_bodies = [article.body for article in self.training_data]
        training_training_gram_matrix = kernel.gram_matrix(training_bodies, training_bodies)
        testing_training_gram_matrix = kernel.gram_matrix(row_arguments=test_bodies, column_arguments=training_bodies)
        training_classifications = [topic.value in article.topics for article in self.training_data]
        print(training_classifications)
        support_vector_machine = svm.SVC(kernel='precomputed')
        support_vector_machine.fit(training_training_gram_matrix, training_classifications)
        expected_classifications = [topic.value in article.topics for article in self.test_data]
        assert not all([c == expected_classifications[0] for c in expected_classifications])
        actual_classifications = support_vector_machine.predict(testing_training_gram_matrix)
        # expected_classifications = [classification == 1 for classification in expected_classifications]
        # actual_classifications = [classification == 1 for classification in actual_classifications]
        return ConfusionMatrix.from_classifications(expected_classifications, actual_classifications)

    @property
    def latex_header(self):
        # TODO
        return "%s & F1 & Precision & Recall \\\\\n" % self.kernel_arg_name

    def evaluation(self, kernel_kwargs=None, output_format=OutputFormat.latex):

        all_rows = ""
        for topic in self.topics:
            for kernel in self.kernels:
                rows = self.__get_rows_for_kernel(kernel, kernel_kwargs, topic, output_format)
                count_rows = len(rows)
                header = "\\multirow{%i}{*}{%s}" % (count_rows, kernel.name())
                all_rows += header + "\n".join(rows)

        return all_rows

    @staticmethod
    def __remove_args_not_understood_by_kernel(kernel, kernel_kwargs):
        kernels_understood_args = kernel.understood_arguments()
        new_kernel_kwargs = kernel_kwargs.copy()
        for key in kernel_kwargs.keys():
            if key not in kernels_understood_args:
                del new_kernel_kwargs[key]
        return new_kernel_kwargs

    def __get_rows_for_kernel(self, kernel, kernel_kwargs, topic, output_format):
        """
        :type kernel_kwargs: dict
        :type kernel: StringKernel
        """
        kernel_kwargs = self.__remove_args_not_understood_by_kernel(kernel, kernel_kwargs)
        if all([type(value) is not list for value in kernel_kwargs.values()]):
            return [self.__get_row_for_kernel(kernel, kernel_kwargs, topic, output_format)]
        for key, values in kernel_kwargs.items():
            if type(values) is list:
                rows = []
                for value in values:
                    new_kernel_kwargs = kernel_kwargs.copy()
                    new_kernel_kwargs[key] = value
                    rows += self.__get_rows_for_kernel(kernel, new_kernel_kwargs, topic, output_format)
                return rows  # Other iterable args will have already been taken care of in the recursion

    def __get_row_for_kernel(self, kernel, kernel_kwargs, topic, output_format):
        confusion_matrix = self.confusion_matrix(kernel, kernel_kwargs, topic)
        kernel_args = [str(kernel_arg) for kernel_arg in kernel_kwargs.values()]
        f1 = str(confusion_matrix.f1)
        precision = str(confusion_matrix.precision)
        recall = str(confusion_matrix.recall)
        row = " & " + " & ".join(kernel_args + [f1, precision, recall])
        row_end = " \\\\"
        return row + row_end