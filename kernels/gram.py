__author__ = 'Pontus'
import numpy as np

def gram(docs1, docs2, kernel):
    g = []
    for d1 in docs2:
        g2 = []
        for d2 in docs1:
            g2.append(kernel(d1,d2))
        g.append(np.array(g2))
    return np.array(g)