import numpy as np
import SSK
from math import sqrt

# Beraknar inre Frobeniusprodukten mellan tva Gram-matriser
def frobInnerProd(K1, K2):
	ret = 0.0
	for i in range(0,len(K1)):
		for j in range(0, len(K1[0])):
			tmp1 = K1[i,j]
			tmp2 = K2[i,j]
			ret = ret + (tmp1 * tmp2)
	return ret

# Beraknar "alignment" mellan tva Gram-matriser
def alignment(K1, K2):
	return frobInnerProd(K1, K2) / sqrt(frobInnerProd(K1, K1) * frobInnerProd(K2, K2))

# Hamtar en lista med substrangar av langd n och dess frekvens (onormaliserad) fran S
def getDictionary(S, n):
	ret = dict()
	for s in S:
		offset = 0
		while offset <= len(s)-n:
			tmpStr = s[offset:offset+n]
			if not ret.has_key(tmpStr):
				ret[tmpStr] = 0
			ret[tmpStr] += 1
			offset += 1
	return ret

# Hamtar de x vanligaste substrangarna av langd n fran S
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

#Om Dictionary D redan beraknad, anvand denna:
def getSubsetD(S, n, x, D):
	dictionary = D
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

# Returnerar forhoppningsvis en bra approximation av en Gram-matris
def approxKernelSSK(S, n, x, sskn, sskl):
	s = getSubset(S, n, x)
	ret = np.zeros((len(S), len(S)))
	for i in range(0, len(S)):
		for j in range(0, len(S)):
			tmp = 0
			for st in s:
				tmp += SSK.SSK(sskn, sskl, S[i], st) * SSK.SSK(sskn, sskl, S[j], st)
			ret[i,j] = tmp
	return ret
	
def approxKernelSSKalt(S, n, x, sskn, sskl):
	ret = np.zeros((len(S), len(S)))
	for i in range(0, len(S)):
		for j in range(0, len(S)):
			tmp = 0
			s = getSubset([S[i], S[j]], n, x)
			for st in s:
				tmp += SSK.SSK(sskn, sskl, S[i], st) * SSK.SSK(sskn, sskl, S[j], st)
			ret[i,j] = tmp
	return ret
# Returnerar en exakt Gram-matris
def exactGramSSK(S, sskn, sskl):
	ret = np.zeros((len(S), len(S)))
	for i in range(0, len(S)):
		for j in range(0, len(S)):
			ret[i,j] = SSK.SSK(sskn, sskl, S[i], S[j])
	return ret
