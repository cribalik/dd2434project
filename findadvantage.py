import numpy
from dataset import Dataset
from kernels import SubSequenceStringKernel, NGramsStringKernel
from reuters import DataType

__author__ = 'Daniel Schlaug'

dataset = Dataset()
training = dataset.get_data(topic=None, data_type=DataType.training)
training_bodies = [article.body for article in training]
testing = dataset.get_data(topic=None, data_type=DataType.testing)
testing_bodies = [article.body for article in testing]

length = 5
weight_decay = 0.01

ssk = SubSequenceStringKernel(length, weight_decay)
ngk = NGramsStringKernel(length)

sskgram = ssk.gram_matrix(row_arguments=training_bodies, column_arguments=testing_bodies)
ngkgram = ngk.gram_matrix(training_bodies, testing_bodies)
results = []

used_coordinates = set()
for _ in range(0, 100):
    max_advantage = sskgram[0, 0] - ngkgram[0, 0]
    best_coordinates = (0, 0)
    for row in range(0, 380):
        for column in range(0, 90):
            if (row, column) in used_coordinates:
                continue
            advantage = sskgram[row, column] - ngkgram[row, column]
            if advantage > max_advantage:
                max_advantage = advantage
                best_coordinates = (row, column)
    article1 = training[best_coordinates[0]]
    article2 = testing[best_coordinates[1]]
    result = {"advantage": max_advantage,
              "coordinates": best_coordinates,
              "doc1": "%s: %s" % (article1.topics, article1.body),
              "doc2": "%s: %s" % (article2.topics, article2.body),}
    results.append(result)
    used_coordinates.add(best_coordinates)

print("Length: %f, weight decay: %f" % (length, weight_decay))

for result in results:
    print("\nAdvantage: %f, indices: %s" % (result['advantage'], result['coordinates']))
    print()
    print(result['doc1'])
    print()
    print(result['doc2'])