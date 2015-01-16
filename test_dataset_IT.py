from dataset import *
from unittest import TestCase

__author__ = 'Daniel Schlaug'


class TestDataset(TestCase):
    def test_get_data(self):
        dataset = Dataset()
        article_set = set()
        for topic in Topics:
            for data_type in DataType:
                for article in dataset.get_data(topic, data_type):
                    article_set.add(article)
        self.failUnlessEqual(470, len(article_set))

        # Test that all topics exist
        for type in [DataType.testing, DataType.training]:
            for topic in Topics:
                found = False
                for article in article_set:
                    if article.data_type == type and topic.value in article.topics:
                        found = True
                        break
                self.failUnless(found, "Did not find any article with topic: %s, type: %s" % (topic.value, type.name))