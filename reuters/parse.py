from lxml.etree import XMLSyntaxError

__author__ = 'Daniel Schlaug'

import os
import re

from article import Article
from article import DataType
from reuters import split

from lxml import etree


class Parser:
    def __init__(self, reuters_location, remove_stopwords=True, remove_punctuation=True, remove_pattern=r"\d",
                 split_function=split.modapte):
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
        self.__remove_pattern = re.compile(remove_pattern) if remove_pattern else False
        self.__split = split_function
        self.__cached_articles = None

    def articles(self, only_of_type=None, with_topics=None, without_topics=None, limit_count_to=None):
        """
        Parse and return the articles in the reuters data set.

        :type only_of_type: DataType
        :param only_of_type: Optional. Pass a DataType to get only articles of that type.
        :rtype : List(T <= Article)
        :return: All articles in the data set.
        """
        if not self.__cached_articles:
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
            self.__cached_articles = articles
        articles = self.__cached_articles
        if only_of_type:
            articles = [article for article in articles if article.data_type == only_of_type]
        if with_topics:
            included_topics = with_topics
            articles = [article for article in articles if all([topic in article.topics for topic in included_topics])]
        if without_topics:
            excluded_topics = without_topics
            articles = [article for article in articles if
                        all([topic not in article.topics for topic in excluded_topics])]
        if limit_count_to or limit_count_to == 0:
            articles = articles[0:limit_count_to]
        return articles

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

    def __parse_sgm_file(self, sgm_file_path):
        resilient_parser = etree.XMLParser(recover=True, encoding='ascii')

        with open(sgm_file_path) as sgm_file:
            sgm_file.readline()
            file_contents = sgm_file.read()

        file_contents = re.sub(r'...&#5;&#30;', '', file_contents)  # Hack to get past nasty character in reut2-017.sgm
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

    def __scrub(self, text):
        if self.__remove_punctuation:
            text = re.sub(self.__punctuation_pattern, '', text)
            if self.__remove_pattern:
                text = re.sub(self.__remove_pattern, '', text)
            text = re.sub(r'\s+', ' ', text)
        if self.__remove_stopwords:
            stopwords = self.stop_list
            text = ' '.join([word for word in text.lower().split() if word not in stopwords])
        return text