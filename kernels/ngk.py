# coding=utf-8
import numpy as np

__author__ = 'Pontus'

# n is the size of the n-grams used.
# docstring1 and docstring2 are document strings with stop words and '.' removed
# ngk(n)(docstring1, docstring2)
def ngkernel(x, y, n, weighted=False):
    if not weighted:
        n_grams_in_x = set()
        n_grams_in_y = set()

        for i in range(len(x)):
            n_grams_in_x.add(x[i:i+n])

        for i in range(len(y)):
            n_grams_in_y.add(y[i:i+n])

        return len(n_grams_in_x.intersection(n_grams_in_y))
    else:
        n_grams_in_x = dict()
        n_grams_in_y = dict()

        for i in range(len(x)):
            n_gram = x[i:i+n]
            if n_gram not in n_grams_in_x:
                n_grams_in_x[n_gram] = 0
            n_grams_in_x[n_gram] += 1

        for i in range(len(y)):
            n_gram = y[i:i+n]
            if n_gram not in n_grams_in_y:
                n_grams_in_y[n_gram] = 0
            n_grams_in_y[n_gram] += 1

        n_grams_in_both = set(n_grams_in_x.keys()).intersection(set(n_grams_in_y.keys()))
        res = 0
        for n_gram in n_grams_in_both:
            res += n_grams_in_y[n_gram] * n_grams_in_x[n_gram]
        return res


def ngk(n):
    return lambda x, y: ngkernel(x, y, n)



