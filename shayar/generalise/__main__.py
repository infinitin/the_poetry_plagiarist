__author__ = 'Nitin'
import os
import argparse
import cPickle
from threading import Thread
# This import is required for the pickle load
# noinspection PyUnresolvedReferences,PyPep8Naming
import shayar.poem as poem
from n_stanzas_agg import agg_n_stanzas

parser = argparse.ArgumentParser(description='Gather insight on poems.')
parser.add_argument('collection', choices=['test'], help='The particular collection of poems to be analysed.')
parser.add_argument('-plot', type=bool, default=False, metavar='plot',
                    help='If true, shows a plot of every attribute. False by default.')
#parser.add_argument('-nstanzas', type=int, choices=[1, 2, 3], help='Fix the number of stanzas in the poem')

args = parser.parse_args()
f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\analyse', args.collection + '.poems')), 'rb')
poems = cPickle.load(f)
f.close()

# Filter poems here according to parse args
n_stanzas = Thread(target=agg_n_stanzas, args=([p.stanzas for p in poems], args.plot))
n_stanzas.start()