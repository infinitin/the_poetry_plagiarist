__author__ = 'Nitin'
import argparse
import cPickle

parser = argparse.ArgumentParser(description='Gather insight on poems.')

args = parser.parse_args()

poems = cPickle.load('/shayar/analyse/'+args.collection+'.poem')
for poem in poems:
    generalise(poem)