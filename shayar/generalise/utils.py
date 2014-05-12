__author__ = 'Nitin'
import os
import cPickle


#Given the current set of applicable poems and the (new) givens, filter the poems accordingly.
#The keys of the givens correspond exactly to the attributes of the poem template object.
def apply_settings(ps, a, value):
    if a == "n_stanzas":
        ps = [p for p in ps if value == p.stanzas]
    elif a == "lines_per_stanza":
        ps = [p for p in ps if value == p.lines]
    elif a == "repeated_line_locations":
        ps = [p for p in ps if set(value) == p.repeated_lines.values()]
    elif a == "n_repeated_lines":
        ps = [p for p in ps if value == len(p.repeated_lines.values())]
    elif a == "n_distinct_sentences":
        ps = [p for p in ps if value == p.distinct_sentences]
    elif a == "line_tenses":
        ps = [p for p in ps if value == p.tenses]
    elif a == "overall_tense":
        ps = [p for p in ps if value == p.overall_tense]
    elif a == "assonance" or a == "consonance" or a == "alliteration":
        ps = [p for p in ps if value in [d.keys() for d in getattr(p, a)]]
    elif a == "rhyme":
        ps = [p for p in ps if tuple(value) in p.rhyme_scheme]
    elif a == "syllable":
        ps = [p for p in ps if tuple(value) in p.syllable_count]
    elif a == "perspective":
        ps = [p for p in ps if value == p.perspective]

    return ps


#Grab all the poems of a particular collection from store
def retrieve_all_poems(collection):
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\analyse', collection + '.poems')), 'rb')
    poems = cPickle.load(f)
    f.close()
    return poems
