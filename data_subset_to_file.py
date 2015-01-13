__author__ = 'Daniel Schlaug'

from reuters import DataType
from dataset import Topics, Dataset
import os

__author__ = 'cmarte'

dataset = Dataset()

for path in ["kernels/precomputed/training", "kernels/precomputed/testing"]:
    if not os.path.exists(path):
        os.makedirs(path)

for topic in Topics:
    articles = dataset.get_data(topic=topic, data_type=DataType.training)
    for i, article in enumerate(articles):
        with open("kernels/precomputed/training/" + topic.value + str(i), 'w') as f:
            f.write(article.body)

for topic in Topics:
    articles = dataset.get_data(topic=topic, data_type=DataType.testing)
    for i, article in enumerate(articles):
        with open("kernels/precomputed/testing/" + topic.value + str(i), 'w') as f:
            f.write(article.body)