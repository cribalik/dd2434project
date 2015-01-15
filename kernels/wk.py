import math
import numpy as np
from scipy import spatial
__author__ = 'Pontus'

# docs is an array of document strings with stop words an '.' removed
# docstring1 and docstring2 are document strings in docs
# idf = get_idf(docs)
# wk(idf)(docstring1, docstring2)


def wkernel(x, y, idf):
    wx = x.split(" ")
    wy = y.split(" ")
    words_in_x = dict()
    words_in_y = dict()

    for word in wx:
        if word not in words_in_x:
            words_in_x[word] = 0
        words_in_x[word] += 1

    for word in wy:
        if word not in words_in_y:
            words_in_y[word] = 0
        words_in_y[word] += 1

    words_from_both = set(words_in_x.keys()).union(set(words_in_y.keys()))

    words_from_both = list(words_from_both)
    weighted_x = [math.log(1. + words_in_x[key]) * math.log(idf[key]) if key in words_in_x else 0. for key in words_from_both]
    weighted_y = [math.log(1. + words_in_y[key]) * math.log(idf[key]) if key in words_in_y else 0. for key in words_from_both]

    return 1 - spatial.distance.cosine(weighted_x, weighted_y)


def wk(idf):
    return lambda x, y: wkernel(x, y, idf)


def get_df(docs):
    df = {}
    for d in docs:
        dw = d.split(" ")
        for w in set(dw):
            if w in df:
                df[w] += 1.
            else:
                df[w] = 1.
    return df


# Takes an array of document strings and returns a dict with words as key and idf as value
def get_idf(docs):
    n = len(docs)
    df = get_df(docs)
    for key in df:
        df[key] = n/df[key]
    return df

