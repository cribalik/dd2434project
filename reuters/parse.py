from lxml.etree import XMLSyntaxError

__author__ = 'Daniel Schlaug'

import os
import re

from article import Article
from reuters import split

from lxml import etree


class Parser:
    def __init__(self, reuters_location, remove_stopwords=True, remove_punctuation=True, split_function=split.modapte):
        """
        Create a new parser for the Reuters data set.

        :type reuters_location: str
        :type remove_stopwords: bool
        :type remove_punctuation: bool
        :param reuters_location: str An optional string with the path of the root for the data set (containing all the
        sgm files) or of a single sgm file to use.
        :param split_function: The function to be used to determine the DataType of each article.
        :return: Parser A new parser.
        """
        if not os.path.exists(reuters_location):
            raise Exception("Could not create reuters.Parser because path %r was not found." % reuters_location)
        if os.path.isfile(reuters_location) and not reuters_location.lower().endswith(".sgm"):
            raise Exception(
                "Could not create reuters.Parser because %r is not a directory or sgm file." % reuters_location)

        self.__reuters_location = reuters_location
        self.__remove_stopwords = remove_stopwords
        self.__remove_punctuation = remove_punctuation
        self.__stop_list = None
        self.__punctuation_pattern = re.compile(r'[^\w\s]')
        self.__split = split_function

    def articles(self):
        """
        Parse and return the articles in the reuters data set.

        :rtype : List(T <= Article)
        :return: All articles in the data set.
        """
        if os.path.isdir(self.__reuters_location):
            data_files = os.listdir(self.__reuters_location)
            sgm_files = filter(lambda filename: filename.lower().endswith(".sgm"), data_files)
        else:
            sgm_files = [self.__reuters_location]
        articles = []
        for sgm_file in sgm_files:
            full_file_path = os.path.join(self.__reuters_location, sgm_file)
            articles_in_file = self.__parse_sgm_file(full_file_path)
            articles += articles_in_file
        return articles

    def __parse_sgm_file(self, sgm_file_path):
        resilient_parser = etree.XMLParser(recover=True, encoding='ascii')

        with open(sgm_file_path) as sgm_file:
            sgm_file.readline()
            file_contents = sgm_file.read()

        file_contents = re.sub(r'...&#5;&#30;', '', file_contents) # Hack to get past nasty character in reut2-017.sgm
        file_contents = "<articles>" + file_contents + "</articles>"
        try:
            xml_tree = etree.fromstring(file_contents, resilient_parser)
        except (XMLSyntaxError, ValueError) as e:
            raise Exception("Could not parse file %s:\n%s" % (sgm_file_path, e.message))

        xml_articles = xml_tree
        articles = []
        for xml_element in xml_articles.iterchildren():
            article = self.__parse_reuters_element(xml_element)
            if article:
                articles.append(article)
            else:
                print("Could not parse element \n %r" % etree.tostring(xml_element))
        return articles

    def __parse_reuters_element(self, reuters_element):
        data_type = self.__split(reuters_element)
        assert data_type is not None, "Data type should never be None (should instead be unused)"
        topics = reuters_element.xpath('.//TOPICS/D/text()')
        body_texts = reuters_element.xpath('.//TEXT/text() | .//TEXT/TITLE/text() | .//TEXT/BODY/text()')
        body = '\n'.join(body_texts)
        scrubbed_body = self.__scrub(body)
        if len(scrubbed_body) == 0:
            print("Warning: Empty element: %r" % etree.tostring(reuters_element))
        return Article(topics=topics, body=scrubbed_body, data_type=data_type)

    @property
    def stop_list(self):
        if not self.__stop_list:
            import nltk

            def fetch_stopwords():
                return set(nltk.corpus.stopwords.words('english'))

            try:
                self.__stop_list = fetch_stopwords()
            except LookupError:
                nltk.download('stopwords')
                self.__stop_list = fetch_stopwords()
        return self.__stop_list

    def __scrub(self, text):
        if self.__remove_punctuation:
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(self.__punctuation_pattern, '', text)
        if self.__remove_stopwords:
            stopwords = self.stop_list
            text = ' '.join([word for word in text.lower().split() if word not in stopwords])
        return text