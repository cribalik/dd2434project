import numpy
from dataset import Dataset
from kernels import SubSequenceStringKernel, NGramsStringKernel
from reuters import DataType

__author__ = 'Daniel Schlaug'

dataset = Dataset()
training = dataset.get_data(topic=None, data_type=DataType.training)
training_bodies = [article.body for article in training]

length = 14
weight_decay = 0.01

kernel = SubSequenceStringKernel(length, weight_decay)
kernel = NGramsStringKernel(length)

gram = kernel.gram_matrix(training_bodies, training_bodies)
results = []
for _ in range(0, 100):
    max_similarity = gram[0, 1]
    best_coordinates = (0, 1)
    for row in range(0, 380):
        for column in range(0, 380):
            similarity = gram[row, column]
            if row == column or similarity == 1:
                continue
            if similarity > max_similarity:
                max_similarity = similarity
                best_coordinates = (row, column)
    result = {"similarity": max_similarity,
              "coordinates": best_coordinates,
              "doc1": training[best_coordinates[0]].body,
              "doc2": training[best_coordinates[1]].body}
    results.append(result)
    gram[best_coordinates] = 0
    gram[best_coordinates[1], best_coordinates[0]] = 0

print("Length: %f, weight decay: %f" % (length, weight_decay))

for result in results:
    print("\nSimilarity: %f, indices: %s" % (result['similarity'], result['coordinates']))
    print()
    print(result['doc1'])
    print()
    print(result['doc2'])