from enum import Enum

__author__ = 'Daniel Schlaug'


class DataType(Enum):
    training = 1
    testing = 2
    unused = 3

class Article:
    def __init__(self, body, topics, data_type, id):
        """
        Create a new article.

        :param body: A string with the body of the article.
        :param topics: A set of strings representing the topics for the article.
        :param data_type: Whether the article is used for training, testing or unused.
        :type body: str
        :type topics: List(T <= str)
        :type data_type: DataType
        :return: A new article object.
        """
        self.__body = body
        self.__topics = topics
        self.__data_type = data_type
        self.__id = id

    @property
    def body(self):
        """
        :rtype : str
        """
        return self.__body

    @property
    def topics(self):
        """
        :rtype : List(T <= str)
        """
        return self.__topics

    @property
    def data_type(self):
        """
        :rtype : DataType
        """
        return self.__data_type

    @property
    def id(self):
        """
        :rtype : str
        """
        return self.__id