from unittest import TestCase

from reuters.parse import *
from bs4 import BeautifulSoup


__author__ = 'Daniel Schlaug'

_dir = os.path.dirname(__file__)

_path_to_real_reuters = os.path.join(_dir, "../data/reuters21578")


class TestParserIT(TestCase):
    _parser_stopwords_punctuation_removed_modapte = None

    @property
    def parser_stopwords_punctuation_removed_modapte(self):
        if TestParserIT._parser_stopwords_punctuation_removed_modapte is None:
            parser = Parser(_path_to_real_reuters,
                            remove_punctuation=True,
                            remove_stopwords=True,
                            split_function=split.modapte)
            TestParserIT._parser_stopwords_punctuation_removed_modapte = parser
        return TestParserIT._parser_stopwords_punctuation_removed_modapte

    def test_number_of_unused_articles(self):
        parser = self.parser_stopwords_punctuation_removed_modapte
        unused_articles = parser.articles(only_of_type=DataType.unused)
        self.failUnlessEqual(8676, len(unused_articles))

    def test_number_of_test_articles(self):
        parser = self.parser_stopwords_punctuation_removed_modapte
        test_articles = parser.articles(only_of_type=DataType.testing)
        self.failUnlessEqual(3299, len(test_articles))

    def test_number_of_training_articles(self):
        parser = self.parser_stopwords_punctuation_removed_modapte
        training_articles = parser.articles(only_of_type=DataType.training)
        self.failUnlessEqual(9603, len(training_articles))

    def test_number_of_articles_in_each_file(self):
        data_files = os.listdir(_path_to_real_reuters)
        sgm_files = filter(lambda filename: filename.lower().endswith(".sgm"), data_files)
        for sgm_file in sgm_files:
            parser = Parser(os.path.join(_path_to_real_reuters, sgm_file),
                            remove_stopwords=True,
                            remove_punctuation=True,
                            split_function=split.modapte)
            articles = parser.articles()
            expected_n_articles = 578 if "021" in sgm_file else 1000
            self.failUnlessEqual(len(articles), expected_n_articles, "Failed on %r" % sgm_file)

    def test_annoying_reut2_017(self):
        path = os.path.join(_path_to_real_reuters, "reut2-017.sgm")
        annoying_file = open(path)
        soup = BeautifulSoup(annoying_file)
        all_text = soup.find_all("text")
        self.failUnlessEqual(len(all_text), 1000)
        parser = Parser(path,
                        remove_stopwords=False,
                        remove_punctuation=False,
                        split_function=split.modapte)
        articles = parser.articles()
        for article in articles:
            condition = True
            while condition:
                text_element = all_text.pop(0)
                soup_got = filter(lambda s: len(s) > 0, text_element.get_text().split("\n"))[0]
                parser_got = filter(lambda s: len(s) > 0, article.body.split("\n"))[0]
                soup_got = re.sub(r'[<>]', '', soup_got)
                parser_got = re.sub(r'[<>]', '', parser_got)
                if not soup_got[0:3] == parser_got[0:3]:
                    print("Missmatch: %r, %r" % (soup_got, parser_got))
                else:
                    condition = False
        self.failUnlessEqual(len(all_text), 0)