from dataset import Dataset
from kernelevaluater import KernelEvaluater, OutputFormat
from kernels import NGramsStringKernel, SubSequenceStringKernel
from reuters import DataType

__author__ = 'Daniel Schlaug'

lengths = [3, 4, 5, 6, 7, 8, 10, 12, 14]
weight_decays = [0.01, 0.03, 0.05, 0.07, 0.09, 0.1, 0.3, 0.5, 0.7, .9]

kernels = [SubSequenceStringKernel]#, NGramsStringKernel]

dataset = Dataset()
training_data = dataset.get_data(topic=None, data_type=DataType.training)
test_data = dataset.get_data(topic=None, data_type=DataType.testing)

evaluator = KernelEvaluater(training_data=training_data, test_data=test_data, kernels=kernels)

print(evaluator.evaluation(kernel_kwargs={'n': lengths, 'length': lengths, 'weight_decay': 0.5}, output_format=OutputFormat.latex))