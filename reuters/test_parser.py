__author__ = 'Daniel Schlaug'
from unittest import TestCase
import os

from reuters import *


_dir = os.path.dirname(__file__)


def _get_test_articles():
    parser = Parser(os.path.join(_dir, "testroot"))
    return parser.articles()


class TestParser(TestCase):

    def test_number_of_articles(self):
        articles = _get_test_articles()
        self.failUnlessEqual(len(articles), 27)

    def test_article_body(self):
        articles = _get_test_articles()
        beginning_of_first_body = "uk money market shortage forecast 250 mln stg bank england said for"
        self.failUnlessEqual(beginning_of_first_body, articles[0].body[0:len(beginning_of_first_body)])
        end_of_last_body = " year gave details reuter"
        self.failUnlessEqual(end_of_last_body, articles[-1].body[-25:])

    def test_article_topics(self):
        articles = _get_test_articles()
        topics_of_second_item = ["money-fx", "interest"]
        self.failUnlessEqual(topics_of_second_item, articles[1].topics)

    def test___scrub(self):
        parser = Parser(os.path.join(_dir, "testroot"))
        self.failUnlessEqual("details reuter", parser._Parser__scrub(" no further details.\n REUTER\n"))