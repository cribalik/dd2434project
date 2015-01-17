from unittest import TestCase
from dataset import Dataset, Topics
from reuters import DataType
from kernels.ngk import ngkernel

__author__ = 'Daniel Schlaug'


class TestNgkernelIT(TestCase):
    def test_ngkernel_orthogonal_data(self):
        dataset = Dataset()
        for topic in Topics:
            training_bodies = [article.body for article in dataset.get_data(topic=topic, data_type=DataType.training)]
            testing_bodies = [article.body for article in dataset.get_data(topic=topic, data_type=DataType.testing)]

            evaluations = 0
            perpendicular = 0
            for test_body in testing_bodies:
                for training_body in training_bodies:
                    evaluations += 1
                    if ngkernel(test_body, training_body, 14) == 0.0:
                        perpendicular += 1

            print((evaluations, perpendicular))
            self.failIfEqual(evaluations, perpendicular)

    def test_ngkernel_orthogonal_data(self):
        dataset = Dataset()
        training_bodies = [article.body for article in dataset.get_data(topic=None, data_type=DataType.training)]
        testing_bodies = [article.body for article in dataset.get_data(topic=None, data_type=DataType.testing)]

        evaluations = 0
        perpendicular = 0
        for test_body in testing_bodies:
            for training_body in training_bodies:
                evaluations += 1
                if ngkernel(test_body, training_body, 14) == 0.0:
                    perpendicular += 1
                    # print(test_body)
                    # print(training_body)
                    # print("")

        print((evaluations, perpendicular))
        self.failIfEqual(evaluations, perpendicular)