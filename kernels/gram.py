__author__ = 'Pontus'
import numpy as np

def gram(docs, kernel):
    g = []
    for d1 in docs:
        g2 = []
        for d2 in docs:
            g2.append(kernel(d1,d2))
        g.append(np.array(g2))
    return np.array(g)