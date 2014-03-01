__author__ = 'Nitin'
import os
import argparse
import cPickle
# This import is required for the pickle load to work
# noinspection PyUnresolvedReferences,PyPep8Naming
import shayar.poem as poem


def generalise(analysed_poem):
    print str(analysed_poem)


parser = argparse.ArgumentParser(description='Gather insight on poems.')
parser.add_argument('collection', choices=['test'], help='The particular collection of poems to be analysed')
#parser.add_argument('-nstanzas', type=int, choices=[1, 2, 3], help='The number of stanzas in the poem')

args = parser.parse_args()
f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\analyse', args.collection + '.poems')), 'rb')
poems = cPickle.load(f)
f.close()

# Filter poems here according to parse args

for p in poems:
    generalise(p)