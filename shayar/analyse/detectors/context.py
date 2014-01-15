__author__ = 'Nitin'

from nltk.sem.drt import *
from nltk.parse import load_parser
from utils import get_tokenized_words
from nltk.featstruct import FeatStructParser
from nltk.grammar import FeatStructNonterminal
from shayar.drt import grammar_dir


def build_drs(poem):
    #parser = load_parser('file:' + grammar_dir.replace('\\', '/'), trace=0, fstruct_parser=FeatStructParser(fdict_class=FeatStructNonterminal, logic_parser=DrtParser()))
    parser = load_parser('file:' + grammar_dir.replace('\\', '/'), trace=0, logic_parser=DrtParser())

    words = []
    for line in poem:
        words.extend(get_tokenized_words(line))

    #trees = parser.nbest_parse(line)
    trees = parser.nbest_parse('All dogs like John'.split())
    if not trees: print 'no way to parse this!'
    for tree in trees:
        print(tree.node['SEM'].simplify())