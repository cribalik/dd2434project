from unittest import TestCase
from parse import *

__author__ = 'Daniel Schlaug'


class TestParser(TestCase):
    def test_articles(self):
        self.failUnlessEqual(test, 67)
        parser = Parser("testroot")
        articles = parser.articles()
        self.failUnlessEqual(len(articles), 2)
