import numpy as np
from math import sqrt

# Beräknar inre Frobeniusprodukten mellan två Gram-matriser
def frobInnerProd(K1, K2):
	ret = 0
	for i in range(0,len(K1)):
		for j in range(0, len(K1[0])):
			ret += K1[i,j] * K2[i,j]
	return ret

# Beräknar "alignment" mellan två Gram-matriser
def alignment(K1, K2):
	return frobInnerProd(K1, K2) / sqrt(frobInnerProd(K1, K1) * frobInnerProd(K2, K2))

# Hämtar en lista med substrängar av längd n och dess frekvens (onormaliserad) från S
def getDictionary(S, n):
	ret = dict()
	offset = 0
	while offset < len(S)-n:
		tmpStr = S[offset:offset+n]
		if not ret.has_key(tmpStr):
			ret[tmpStr] = 0
		ret[tmpStr] += 1
		offset += 1
	return ret

# Hämtar de x vanligaste substrängarna av längd n från S
def getSubset(S, n, x):
	dictionary = getDictionary(S, n)
	ret = []
	smallest = 999999
	smallInd = 0
	for key in dictionary:
		if len(ret) < x:
			ret.append(key)
			if dictionary[key] < smallest:
				smallest = dictionary[key]
				smallInd = len(ret)-1
		else:
			if dictionary[key] > smallest:
				ret[smallInd] = key
				smallest = 999999
				for i in range(0, len(ret)):
					tmpStr = ret[i]
					if dictionary[tmpStr] < smallest:
						smallest = dictionary[tmpStr]
						smallInd = i
	return ret
