__author__ = 'Pontus'

#skapar en dict som matchar floats till ett dokument
def mapa(docs):
    conv = {}
    i= 0.
    for d in docs:
        conv[i] = d
        i = i + 1.
    return conv


def kernel(k, conv):
    return lambda x, y: k(conv[x], conv[y])