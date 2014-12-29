__author__ = 'Daniel Schlaug'

class Article:
    def __init__(self, topics, body):
        """
        Create an article from its category and list of words.

        :param topics: A set of strings representing the topics for the article.
        :param body: A string with the body of the article.
        :return: A new article object.
        """
        self.__topics = topics
        self.__body = body

    @property
    def body(self):
        return self.__body

    @property
    def topics(self):
        return self.__topics