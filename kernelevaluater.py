from collections import OrderedDict
from multiprocessing.pool import Pool
import traceback

from enum import Enum
from sklearn import svm
import sys

from confusionmatrix import ConfusionMatrix
from dataset import Topics


__author__ = 'Daniel Schlaug'


class OutputFormat(Enum):
    latex = 'LaTeX'
    python = 'python'


def confusion_matrix_from(test_data, training_data, kernel, kernel_kwargs, topic):
    valid_kernel_kwargs = KernelEvaluater._remove_args_not_understood_by_kernel(kernel, kernel_kwargs)
    assert set(valid_kernel_kwargs.keys()) == set(
        kernel.understood_arguments()), "Kernel %s got arguments %s, expected %s" % (
        kernel.name, valid_kernel_kwargs.keys(), kernel.understood_arguments())
    kernel = kernel(**valid_kernel_kwargs)
    test_bodies = [article.body for article in test_data]
    training_bodies = [article.body for article in training_data]
    training_training_gram_matrix = kernel.gram_matrix(training_bodies, training_bodies)
    testing_training_gram_matrix = kernel.gram_matrix(row_arguments=test_bodies, column_arguments=training_bodies)
    training_classifications = [topic in article.topics for article in training_data]
    assert_topic_order(training_data)
    assert all(classification in training_classifications for classification in [True, False])
    support_vector_machine = svm.SVC(kernel='precomputed')
    support_vector_machine.fit(training_training_gram_matrix, training_classifications)
    expected_classifications = [topic in article.topics for article in test_data]
    assert_topic_order(test_data)
    actual_classifications = support_vector_machine.predict(testing_training_gram_matrix)
    return ConfusionMatrix.from_classifications(expected_classifications, actual_classifications)


def _get_row_for_kernel(test_data, training_data, kernel, kernel_kwargs, topic):
    try:
        confusion_matrix = confusion_matrix_from(test_data, training_data, kernel, kernel_kwargs, topic)
        row = OrderedDict([("topic", topic), ("kernel", kernel.name())] + kernel_kwargs.items())
        row["f1"] = confusion_matrix.f1
        row["precision"] = confusion_matrix.precision
        row["recall"] = confusion_matrix.recall
        return row
    except:
        # Put all exception text into an exception and raise that
        raise Exception("".join(traceback.format_exception(*sys.exc_info())))


class KernelEvaluater:
    def __init__(self, training_data, test_data, kernels, topics=Topics.values()):
        self.training_data = training_data
        self.test_data = test_data
        self.kernels = kernels
        self.topics = topics

    @staticmethod
    def __latex_header(rows):
        row = rows[0]
        prefix = ""
        items = " & ".join([str(key).replace('_', ' ').title() for key in row.keys()])
        suffix = ""
        return prefix + items + suffix

    def evaluation(self, kernel_kwargs=None, output_format=OutputFormat.python):
        pending_rows = []

        processing_pool = Pool()

        for topic in self.topics:
            for kernel in self.kernels:
                pending_rows += self.__get_rows_for_kernel(kernel, kernel_kwargs, topic, processing_pool)

        rows = [pending_row.get() for pending_row in pending_rows]

        if output_format == OutputFormat.python:
            return rows
        elif output_format == OutputFormat.latex:
            header = KernelEvaluater.__latex_header(rows)

            lines = [" & ".join(["%.4f" % value if type(value) is float else str(value) for value in row.values()]) for
                     row in rows]
            return " \\\\\n".join([header] + lines)

    @staticmethod
    def _remove_args_not_understood_by_kernel(kernel, kernel_kwargs):
        kernels_understood_args = kernel.understood_arguments()
        new_kernel_kwargs = kernel_kwargs.copy()
        for key in kernel_kwargs.keys():
            if key not in kernels_understood_args:
                del new_kernel_kwargs[key]
        return new_kernel_kwargs

    @staticmethod
    def _zero_out_args_not_understood_by_kernel(kernel, kernel_kwargs):
        kernels_understood_args = kernel.understood_arguments()
        new_kernel_kwargs = kernel_kwargs.copy()
        for key in kernel_kwargs.keys():
            if key not in kernels_understood_args:
                new_kernel_kwargs[key] = None
        return new_kernel_kwargs

    def __get_rows_for_kernel(self, kernel, kernel_kwargs, topic, processing_pool):
        """
        :type kernel_kwargs: dict
        :type kernel: StringKernel
        """
        kernel_kwargs = self._zero_out_args_not_understood_by_kernel(kernel, kernel_kwargs)
        if all([type(value) is not list for value in kernel_kwargs.values()]):
            return [
                processing_pool.apply_async(_get_row_for_kernel, (self.test_data, self.training_data, kernel, kernel_kwargs, topic))]
        for key, values in kernel_kwargs.items():
            if type(values) is list:
                pending_rows = []
                for value in values:
                    new_kernel_kwargs = kernel_kwargs.copy()
                    new_kernel_kwargs[key] = value
                    pending_rows += self.__get_rows_for_kernel(kernel, new_kernel_kwargs, topic, processing_pool)
                return pending_rows  # Other iterable args will have already been taken care of in the recursion


def assert_topic_order(articles):
    seen_topics = []
    for article in articles:
        topic = [topic for topic in article.topics if topic in Topics.values()][0]
        if len(seen_topics) == 0 or seen_topics[-1] != topic:
            seen_topics.append(topic)
    assert seen_topics == Topics.values()