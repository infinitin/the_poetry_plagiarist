__author__ = 'Nitin'

from nltk.corpus import wordnet
from pattern.text.en import pluralize
import itertools

HEADING = "#############################\n"
NOUN_RULE = "N[NUM=%s,SEM=<\\x.DRS([],[%s(x)])>] -> '%s'\n"
PRONOUN_RULE = "PropN[%sLOC,NUM=%s,SEM=<\P.(DRS([x],[%s(x)])+P(x))>] -> '%s'\n"


def write_all_rules(grammar_file):
    grammar_file.write(HEADING)
    grammar_file.write("# Nouns\n")
    grammar_file.write(HEADING)
    grammar_file.write("\n")
    write_noun_rules(grammar_file)

    grammar_file.write("\n")
    grammar_file.write(HEADING)
    grammar_file.write("# Proper Nouns\n")
    grammar_file.write(HEADING)
    grammar_file.write("\n")
    write_proper_noun_rules(grammar_file)


def write_noun_rules(grammar_file):
    for synset in wordnet.all_synsets(wordnet.NOUN):
        for lemma in synset.lemmas:

            if not lemma.name[0].islower():
                continue

            plurals = set([pluralize(lemma.name, classical=False), pluralize(lemma.name, classical=False)])
            if not plurals:
                grammar_file.write(NOUN_RULE % ('ms', lemma.name, lemma.name.replace('_', ' ')))
            else:
                grammar_file.write(NOUN_RULE % ('sg', lemma.name, lemma.name.replace('_', ' ')))
                for plural in plurals:
                    grammar_file.write(NOUN_RULE % ('pl', lemma.name, plural.replace('_', ' ')))


def write_proper_noun_rules(grammar_file):
    for synset in wordnet.all_synsets(wordnet.NOUN):
        for lemma in synset.lemmas:
            if not lemma.name[0].islower():
                    grammar_file.write(PRONOUN_RULE % ('-', 'sg', lemma.name.replace('_', ' '), lemma.name.replace('_', ' ')))
