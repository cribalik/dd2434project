from enum import Enum
from SSK import SSKfile
from SSK import SSKfiles
import subprocess

__author__ = "Christopher Martensson"

class DataType(Enum):
	training = 'training'
	testing = 'testing'

class Topics(Enum):
    earn = 'earn'
    acquisition = 'acq'
    crude = 'crude'
    corn = 'corn'

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

test_files = []
training_files = []

for topic in Topics:
	for i in xrange( count_dictionary[topic][DataType.training] ):
		training_files.append( '/home/christopher/dd2434project/kernels/precomputed/training/' + topic.value + str(i) )

for topic in Topics:
  for i in xrange( count_dictionary[topic][DataType.testing] ):
    test_files.append( '/home/christopher/dd2434project/kernels/precomputed/testing/' + topic.value + str(i) )

for plambda in [0.01, 0.03, 0.05, 0.07, 0.09, 0.1, 0.3, 0.5, 0.7, 0.9]:
	with open("SSK-2-lambda"+str(plambda)+".txt",'w') as f:
		for file1 in test_files:
			print file1
			print plambda
			v = SSKfiles(5, file1, training_files, plambda)
			# v = [str(SSKfile(length, file1, file2, 0.5)) for file2 in training_files]
			f.write(','.join(v))
			f.write('\n')
