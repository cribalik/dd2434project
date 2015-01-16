from enum import Enum
from SSK import SSKfiles

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

training_files = []

for topic in Topics:
	for i in xrange( count_dictionary[topic][DataType.training] ):
		training_files.append( '/home/christopher/dd2434project/kernels/precomputed/training/' + topic.value + str(i) )

for length in [5,6,7,8,10,12,14]:
	with open("SSK-length"+str(length)+".txt",'w') as f:
		for file1 in training_files:
			print file1
			print length
			v = SSKfiles(length, file1, training_files, 0.5)
			# v = [str(SSKfile(length, file1, file2, 0.5)) for file2 in training_files]
			f.write(','.join(v))
			f.write('\n')

