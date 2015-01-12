from enum import Enum

from reuters import Parser, DataType


__author__ = 'Daniel Schlaug'


class Topics(Enum):
    earn = 'earn'
    acquisition = 'acq'
    crude = 'crude'
    corn = 'corn'


class Dataset:
    """
    Examlple usage:
    dataset = Dataset()
    acquisition_training_set = dataset.get_data(DataType.training, Topics.acquisition)
    """
    def __init__(self, reuters_path="data/reuters21578"):
        self.parser = Parser(reuters_path)

    def get_data(self, topic, data_type):
        count_dictionary = {
            Topics.earn: {DataType.training: 152,
                          DataType.testing: 40},
            Topics.acquisition: {DataType.training: 114,
                                 DataType.testing: 25},
            Topics.crude: {DataType.training: 76,
                           DataType.testing: 15},
            Topics.corn: {DataType.training: 38,
                          DataType.testing: 10}
        }
        included_topic = topic
        count = 0
        if included_topic in count_dictionary and data_type in count_dictionary[included_topic]:
            count = count_dictionary[included_topic][data_type]
        included_topics = [included_topic.value]
        excluded_topics = [excluded_topic.value for excluded_topic in Topics if excluded_topic != included_topic]
        articles = self.parser.articles(only_of_type=data_type,
                                        with_topics=included_topics,
                                        without_topics=excluded_topics,
                                        limit_count_to=count)
        assert len(articles) == count, "Wrong count on topic: %r, data_type: %r: %i" % (topic, data_type, len(articles))
        return articles