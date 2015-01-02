from enum import Enum

__author__ = 'Daniel Schlaug'


class DataType(Enum):
    training = 1
    testing = 2
    unused = 3

class Article:
    def __init__(self, body, topics, data_type):
        """
        Create an article from its category and list of words.

        :param body: A string with the body of the article.
        :param topics: A set of strings representing the topics for the article.
        :return: A new article object.
        """
        self.__body = body
        self.__topics = topics
        self.__data_type = data_type

    @property
    def body(self):
        return self.__body

    @property
    def topics(self):
        return self.__topics

    @property
    def data_type(self):
        return self.__data_type