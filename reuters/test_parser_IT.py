from unittest import TestCase
from reuters import DataType

from reuters.parse import *

__author__ = 'Daniel Schlaug'

_dir = os.path.dirname(__file__)

_path_to_real_reuters = os.path.join(_dir, "../data/reuters21578")


class TestParserIT(TestCase):

    _articles_stopwords_punctuation_removed_modapte = None

    @property
    def articles_stopwords_punctuation_removed_modapte(self):
        if TestParserIT._articles_stopwords_punctuation_removed_modapte is None:
            parser = Parser(_path_to_real_reuters, remove_punctuation=True, remove_stopwords=True, split=split.modapte)
            TestParserIT._articles_stopwords_punctuation_removed_modapte = parser.articles()
        return TestParserIT._articles_stopwords_punctuation_removed_modapte

    def test_number_of_unused_articles(self):
        articles = self.articles_stopwords_punctuation_removed_modapte
        unused_articles = [article for article in articles if article.data_type == DataType.unused]
        self.failUnless(len(unused_articles) == 8676, "Wrong number of unused articles: %i" % len(unused_articles))

    def test_number_of_test_articles(self):
        articles = self.articles_stopwords_punctuation_removed_modapte
        test_articles = [article for article in articles if article.data_type == DataType.testing]
        self.failUnless(len(test_articles) == 3299, "Wrong number of testing articles: %i" % len(test_articles))

    def test_number_of_training_articles(self):
        articles = self.articles_stopwords_punctuation_removed_modapte
        training_articles = [article for article in articles if article.data_type == DataType.training]
        self.failUnless(len(training_articles) == 9603, "Wrong number of training articles: %i" % len(training_articles))
