# coding=utf-8
import numpy as np
import math
from scipy import spatial
__author__ = 'Pontus'

# n is the size of the n-grams used.
# docstring1 and docstring2 are document strings with stop words and '.' removed
# ngk(n)(docstring1, docstring2)
def ngkernel(x, y, n, weighted=True):
    if not weighted:
        n_grams_in_x = set()
        n_grams_in_y = set()

        for i in range(len(x)):
            n_grams_in_x.add(x[i:i+n])

        for i in range(len(y)):
            n_grams_in_y.add(y[i:i+n])

        return len(n_grams_in_x.intersection(n_grams_in_y))
    else:
        weighted_n_grams_in_x = dict()
        weighted_n_grams_in_y = dict()
        n_grams_in_x = dict()
        n_grams_in_y = dict()

        #set weights
        for i in range(len(x)):
            n_gram = x[i:i+n]
            if n_gram not in n_grams_in_x:
                n_grams_in_x[n_gram] = 0.
            n_grams_in_x[n_gram] += 1.

        #set weights
        for i in range(len(y)):
            n_gram = y[i:i+n]
            if n_gram not in n_grams_in_y:
                n_grams_in_y[n_gram] = 0.
            n_grams_in_y[n_gram] += 1.

        n_grams_from_both = set(n_grams_in_x.keys()).union(set(n_grams_in_y.keys()))

        norm_y = 0.
        norm_x = 0.
 
        for key in n_grams_from_both:
            if key in n_grams_in_y:
                weighted_n_grams_in_y[key] = (math.log(n_grams_in_y[key])+1.)
            else:
                weighted_n_grams_in_y[key] = 0.
            norm_y += math.pow(weighted_n_grams_in_y[key], 2)

            if key in n_grams_in_x:
                weighted_n_grams_in_x[key] = (math.log(n_grams_in_x[key])+1.)
            else:
                weighted_n_grams_in_x[key] = 0.
            #norm_x += math.pow(weighted_n_grams_in_x[key], 2)


        ###
        #dpne by spatial.distance.cosine
        ###
        #norm_y = math.sqrt(norm_y)
        #norm_x = math.sqrt(norm_x)
        #for key in n_grams_from_both:
        #    if key in n_grams_in_y:
        #        weighted_n_grams_in_y[key] /= norm_y
        #    else:
        #        weighted_n_grams_in_y[key] = 0.
        #    if key in n_grams_in_x:
        #        weighted_n_grams_in_x[key] /= norm_x
        #    else:
        #        weighted_n_grams_in_x[key] = 0.

        return 1 - spatial.distance.cosine(weighted_n_grams_in_x.values(), weighted_n_grams_in_y.values())


def ngk(n):
    return lambda x, y: ngkernel(x, y, n)



