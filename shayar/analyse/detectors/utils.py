__author__ = 'Nitin'

from nltk.corpus import cmudict


def analysis_init():
    global dictionary
    dictionary = cmudict.dict()
    global stressed
    stressed = "1"
    global unstressed
    unstressed = "0"


def get_stanzas(poem):
    stanzas = []
    stanza = []
    for line in poem:
        if not line.strip():
            stanzas.append(stanza)
            stanza = []
        else:
            stanza.append(line)
    stanzas.append(stanza)
    return stanzas