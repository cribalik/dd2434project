from lxml import etree

__author__ = 'Daniel Schlaug'

from reuters.article import DataType

def modapte(reuter_element):
    """
    Classify a reuter element according to the ModApte-split
    (as described in section VIII.B of http://www.daviddlewis.com/resources/testcollections/reuters21578/readme.txt)

    :param reuter_element: The element to classify.
    :type reuter_element: Element
    :return: The DataType of the article or None if the element is not in this split.
    """
    attributes = reuter_element.attrib
    data_type = None
    if 'LEWISSPLIT' in attributes:
        type_string = reuter_element.attrib['LEWISSPLIT']
        if 'TOPICS' in attributes and attributes['TOPICS'] == 'YES':
            if type_string == "TRAIN":
                data_type = DataType.training
            elif type_string == "TEST":
                data_type = DataType.testing
            else:
                data_type = DataType.unused
        else:
            data_type = DataType.unused
    return data_type
