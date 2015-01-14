from unittest import TestCase
from dataset import Topics

__author__ = 'Daniel Schlaug'


class TestTopics(TestCase):
    def test_values(self):
        values = Topics.values()
        self.assertEqual(values, ["acq", "corn", "crude", "earn"])