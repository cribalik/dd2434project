import os
from article import Article

from enum import Enum

try:
    from lxml import etree

    print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree

        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree

            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree

                print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree

                    print("running with ElementTree")
                except ImportError:
                    print("Failed to import ElementTree from any known place")

__author__ = 'Daniel Schlaug'

test = 67


class DataType(Enum):
    training = 1
    testing = 2


class Parser:
    def __init__(self, reuters_location):
        """
        Create a new parser for the Reuters data set.

        :param reuters_location: str A string with the path of the root for the data set (containing all the sgm files).
        :return: Parser A new parser.
        """
        if not os.path.isdir(reuters_location):
            raise Exception("Could not create reuters.Parser because path %r was not found." % reuters_location)

        self.__reuters_location = reuters_location

    def articles(self):
        """
        Parse and return the articles.

        :return: list[Article] All articles in the dataset.
        """
        data_files = os.listdir(self.__reuters_location)
        sgm_files = filter(lambda filename: filename.endswith(".sgm"), data_files)
        articles = []
        for sgm_file in sgm_files:
            full_file_path = os.path.join(self.__reuters_location, sgm_file)
            # event_parser = etree.XMLPullParser(recover=True, events=('start', 'end'))
            resilient_parser = etree.XMLParser(recover=True)
            xml_tree = etree.parse(full_file_path, resilient_parser)
            print(etree.tostring(xml_tree))
            for xml_element in xml_tree.iter():
                if xml_element.tag.upper() == "REUTERS":
                    article = _parse_reuters_element(xml_element)
                    articles.append(article)
        return articles


def _parse_reuters_element(reuters_element):
    title = reuters_element.xpath('//TITLE')
    body = reuters_element.xpath('//BODY')
    large_body = title + body
    assert len(large_body) != 0, "Empty element %r" % reuters_element.tostring()
    return Article(topics=[], body=large_body)