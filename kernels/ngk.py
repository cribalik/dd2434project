# coding=utf-8
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
            n_grams_in_x.add(x[i:i + n])

        for i in range(len(y)):
            n_grams_in_y.add(y[i:i + n])

        return len(n_grams_in_x.intersection(n_grams_in_y))
    else:
        n_grams_in_x = dict()
        n_grams_in_y = dict()

        # set weights
        for i in range(len(x)):
            n_gram = x[i:i + n]
            if n_gram not in n_grams_in_x:
                n_grams_in_x[n_gram] = 0.
            n_grams_in_x[n_gram] += 1.

        # set weights
        for i in range(len(y)):
            n_gram = y[i:i + n]
            if n_gram not in n_grams_in_y:
                n_grams_in_y[n_gram] = 0.
            n_grams_in_y[n_gram] += 1.

        n_grams_from_both = set(n_grams_in_x.keys()).union(set(n_grams_in_y.keys()))
        n_grams_from_both = list(n_grams_from_both)

        weighted_x = [math.log(math.log(n_grams_in_x[key] + 1.)) if key in n_grams_in_x else 0 for key in n_grams_from_both]
        weighted_y = [math.log(math.log(n_grams_in_y[key] + 1.)) if key in n_grams_in_y else 0 for key in n_grams_from_both]

        return 1 - spatial.distance.cosine(weighted_x, weighted_y)


def ngk(n):
    return lambda x, y: ngkernel(x, y, n)



