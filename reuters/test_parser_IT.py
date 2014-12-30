from unittest import TestCase

from reuters.parse import *

__author__ = 'Daniel Schlaug'

_dir = os.path.dirname(__file__)

_path_to_real_reuters = os.path.join(_dir, "../data/reuters21578")


class TestParserIT(TestCase):
    def test_articles(self):
        parser = Parser(_path_to_real_reuters)
        articles = parser.articles()
        self.failUnless(21000 < len(articles) < 22000, "Wrong number of articles: %i" % len(articles))