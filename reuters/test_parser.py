from unittest import TestCase

from reuters.parse import *

__author__ = 'Daniel Schlaug'

__dir = os.path.dirname(__file__)


def _get_test_articles():
    parser = Parser(os.path.join(__dir, "testroot"))
    return parser.articles()


class TestParser(TestCase):
    def test_article_body(self):
        articles = _get_test_articles()
        self.failUnlessEqual(len(articles), 6)
        beginning_of_first_body = "The Bank of England said it forecast a"
        self.failUnlessEqual(beginning_of_first_body, articles[0].body[0:len(beginning_of_first_body)])
        end_of_last_body = "further details.\n REUTER"
        self.failUnlessEqual(end_of_last_body, articles[-1].body[-25:-1])

    def test_article_title(self):
        articles = _get_test_articles()
        self.failUnlessEqual(len(articles), 6)
        first_title = "U.K. MONEY MARKET SHORTAGE FORECAST AT 250 MLN STG"
        self.failUnlessEqual(first_title, articles[0].title)
        second_title = "BANK OF FRANCE SETS MONEY MARKET TENDER"
        self.failUnlessEqual(second_title, articles[1].title)

    def test_article_topics(self):
        articles = _get_test_articles()
        topics_of_second_item = ["money-fx", "interest"]
        self.failUnlessEqual(topics_of_second_item, articles[1].topics)