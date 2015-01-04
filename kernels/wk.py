import math
import numpy as np
from scipy import spatial
__author__ = 'Pontus'


def wkernel(x, y, idf):
    xw = x.split(" ")
    yw = y.split(" ")
    tf = {}

    for w in xw:
        tf[w] = 0.
    for w in yw:
        tf[w] = 0.
    xtf = tf.copy()
    ytf = tf

    #getting tf
    for w in xw:
        if w in xtf:
            xtf[w] += 1.
        else:
            xtf[w] = 1.

    for w in yw:
        if w in ytf:
            ytf[w] += 1.
        else:
            ytf[w] = 1.

    for key in tf:
        ytf[key] = ytf[key] * idf[key]
        xtf[key] = xtf[key] * idf[key]

    #print xtf
    #print xtf.values()
    #print ytf
    #print ytf.values()
    return 1 - spatial.distance.cosine(xtf.values(), ytf.values())


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

def get_idf(docs):
    n = len(docs)
    df = get_df(docs)
    for key in df:
        df[key] = math.log(n/df[key])
    return df

