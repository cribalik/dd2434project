
from collections import OrderedDict
from enum import Enum
from sklearn import svm

from confusionmatrix import ConfusionMatrix
from dataset import Topics

from kernels import NGramsStringKernel

import numpy as np

__author__ = 'Daniel Schlaug'


class OutputFormat(Enum):
    latex = 'LaTeX'
    python = 'python'


class KernelEvaluater:
    def __init__(self, training_data, test_data, kernels, topics=Topics.values()):
        self.training_data = training_data
        self.test_data = test_data
        self.kernels = kernels
        self.topics = topics

    def __kernel_arg_name(self, kwargs):
        kernel_arg_name = self.varying_kernel_args.keys()[0]
        kernel_arg_name = kernel_arg_name.replace('_', ' ').capitalize()
        return kernel_arg_name

    def confusion_matrix(self, kernel, kernel_kwargs, topic):
        valid_kernel_kwargs = KernelEvaluater.__remove_args_not_understood_by_kernel(kernel, kernel_kwargs)
        assert set(valid_kernel_kwargs.keys()) == set(kernel.understood_arguments()), "Kernel %s got arguments %s, expected %s" % (kernel.name, valid_kernel_kwargs.keys(), kernel.understood_arguments())
        kernel = kernel(**valid_kernel_kwargs)
        test_bodies = [article.body for article in self.test_data]
        training_bodies = [article.body for article in self.training_data]
        training_training_gram_matrix = kernel.gram_matrix(training_bodies, training_bodies)
        testing_training_gram_matrix = kernel.gram_matrix(row_arguments=test_bodies, column_arguments=training_bodies)
        training_classifications = [topic in article.topics for article in self.training_data]
        assert all(classification in training_classifications for classification in [True, False])
        support_vector_machine = svm.SVC(kernel='precomputed')
        support_vector_machine.fit(training_training_gram_matrix, training_classifications)
        expected_classifications = [topic in article.topics for article in self.test_data]
        actual_classifications = support_vector_machine.predict(testing_training_gram_matrix)
        # expected_classifications = [classification == 1 for classification in expected_classifications]
        # actual_classifications = [classification == 1 for classification in actual_classifications]
        return ConfusionMatrix.from_classifications(expected_classifications, actual_classifications)

    @staticmethod
    def __latex_header(rows):
        row = rows[0]
        prefix = ""
        items = " & ".join([str(key).title() for key in row.keys()])
        suffix = ""
        return prefix + items + suffix

    def evaluation(self, kernel_kwargs=None, output_format=OutputFormat.python):
        rows = []

        for topic in self.topics:
            for kernel in self.kernels:
                rows += self.__get_rows_for_kernel(kernel, kernel_kwargs, topic, output_format)

        if output_format == OutputFormat.python:
            return rows
        elif output_format == OutputFormat.latex:
            header = KernelEvaluater.__latex_header(rows)

            lines = [" & ".join([str(value) for value in row.values()]) for row in rows]
            return " \\\\\n".join([header] + lines)

    @staticmethod
    def __remove_args_not_understood_by_kernel(kernel, kernel_kwargs):
        kernels_understood_args = kernel.understood_arguments()
        new_kernel_kwargs = kernel_kwargs.copy()
        for key in kernel_kwargs.keys():
            if key not in kernels_understood_args:
                del new_kernel_kwargs[key]
        return new_kernel_kwargs

    @staticmethod
    def __zero_out_args_not_understood_by_kernel(kernel, kernel_kwargs):
        kernels_understood_args = kernel.understood_arguments()
        new_kernel_kwargs = kernel_kwargs.copy()
        for key in kernel_kwargs.keys():
            if key not in kernels_understood_args:
                new_kernel_kwargs[key] = None
        return new_kernel_kwargs

    def __get_rows_for_kernel(self, kernel, kernel_kwargs, topic, output_format):
        """
        :type kernel_kwargs: dict
        :type kernel: StringKernel
        """
        kernel_kwargs = self.__zero_out_args_not_understood_by_kernel(kernel, kernel_kwargs)
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
        row = OrderedDict([("topic", topic), ("kernel", kernel.name())] + kernel_kwargs.items())
        row["f1"] = confusion_matrix.f1
        row["precision"] = confusion_matrix.precision
        row["recall"] = confusion_matrix.recall
        return row
