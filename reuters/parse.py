from lxml.etree import XMLSyntaxError

__author__ = 'Daniel Schlaug'

import os

from enum import Enum

from article import Article

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
        Parse and return the articles in the reuters data set.

        :return: list[Article] All articles in the dataset.
        """
        data_files = os.listdir(self.__reuters_location)
        sgm_files = filter(lambda filename: filename.lower().endswith(".sgm"), data_files)
        articles = []
        for sgm_file in sgm_files:
            full_file_path = os.path.join(self.__reuters_location, sgm_file)
            articles_in_file = _parse_sgm_file(full_file_path)
            articles += articles_in_file
        return articles


def _parse_sgm_file(sgm_file_path):
    resilient_parser = etree.XMLParser(recover=True, encoding='ascii')

    with open(sgm_file_path) as sgm_file:
        sgm_file.readline()
        file_contents = sgm_file.read()

    file_contents = "<articles>" + file_contents + "</articles>"
    try:
        xml_tree = etree.fromstring(file_contents, resilient_parser)
    except XMLSyntaxError as e:
        raise Exception("Could not parse file %s:\n%s" % (sgm_file_path, e.message))
    except ValueError as e:
        raise Exception("Could not parse file %s:\n%s" % (sgm_file_path, e.message))

    xml_articles = xml_tree
    articles = []
    for xml_element in xml_articles.iterchildren("REUTERS"):
        article = _parse_reuters_element(xml_element)
        articles.append(article)
    return articles


def _parse_reuters_element(reuters_element):
    topic_elements = reuters_element.xpath('.//TOPICS/D')
    topics = map(lambda element: element.text, topic_elements)
    title_elements = reuters_element.xpath('.//TITLE')
    if len(title_elements) > 0:
        title_element = title_elements[0]
        title = title_element.text
    else:
        title = None
    body_elements = reuters_element.xpath('.//BODY')
    if len(body_elements) > 0:
        body_element = body_elements[0]
        body = body_element.text
    else:
        body = reuters_element.xpath(".//TEXT")[0].text
    assert len(body) != 0, "Empty element %r" % reuters_element.tostring()
    return Article(topics=topics, body=body, title=title)