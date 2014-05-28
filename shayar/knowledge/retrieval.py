__author__ = 'Nitin'
import os
import cPickle
# This import is required for the pickle load
# noinspection PyUnresolvedReferences,PyPep8Naming


def collocations():
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\knowledge', 'collocations.knowledge')), 'rb')
    knowledge = cPickle.load(f)
    f.close()
    return knowledge