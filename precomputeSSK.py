from reuters import *
from data import *
from kernels.SSK import SSK

n = 5
l = 0.5

dataset = Dataset()

training_articles = [dataset.getData(topic=topic, data_type=DataType.training) for topic in Topics]

with open("SSKpre.txt") as f:
    for a1 in training_articles:
        print(a1.body)
        v = [str(SSK(n, l, a1.body, a2.body)) for a2 in training_articles]
        f.write(','.join(v))
        f.write('\n')

