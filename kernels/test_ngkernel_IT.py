from unittest import TestCase
from dataset import Dataset, Topics
from reuters import DataType
from ngk import ngkernel

__author__ = 'Daniel Schlaug'


class TestNgkernelIT(TestCase):
    def test_ngkernel(self):
        for topic in Topics:
            dataset = Dataset()
            training_bodies = [article.body for article in dataset.get_data(topic=topic, data_type=DataType.training)]
            testing_bodies = [article.body for article in dataset.get_data(topic=topic, data_type=DataType.testing)]

            evaluations = 0
            perpendicular = 0
            for test_body in testing_bodies:
                for training_body in training_bodies:
                    evaluations += 1
                    if ngkernel(test_body, training_body, 14) == 1.0:
                        perpendicular += 1

            self.failIfEqual(evaluations, perpendicular)