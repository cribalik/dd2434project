# coding=utf-8
import numpy as np

__author__ = 'Pontus'

# n is the size of the n-grams used.
# docstring1 and docstring2 are document strings with stop words and '.' removed
# ngk(n)(docstring1, docstring2)
def ngkernel(x, y, n):
    # empty dict
    d = {}

    for i in range(len(x)):
        d[x[i:i+n]] = 0.

    for i in range(len(y)):
        d[y[i:i+n]] = 0.

    xd = d.copy()
    yd = d.copy()

    #This only acounts for if the n-gram exist not how often Borde det vara xd[x[i:i+n]] = xd[x[i:i+n]] + 1 istället.
    for i in range(len(x)):
        xd[x[i:i+n]] = 1.

    for i in range(len(y)):
        yd[y[i:i+n]] = 1.

    #return np.inner(np.array(xd.values()),np.array(yd.values()))
    return np.dot(np.array(xd.values()),np.array(yd.values()).transpose())/len(yd.values())


def ngk(n):
    return lambda x, y: ngkernel(x, y, n)



