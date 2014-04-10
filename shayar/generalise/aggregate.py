__author__ = 'Nitin'
import os
import cPickle
from threading import Thread
# This import is required for the pickle load
# noinspection PyUnresolvedReferences,PyPep8Naming
import shayar.poem as poem
from shayar.poem_template import Template
import argparse
from aggregators.basic_structure import agg_n_stanzas, agg_lines_per_stanza, agg_repeated_line_locations, \
    agg_n_repeated_lines, agg_n_distinct_sentences, agg_line_tenses, agg_overall_tense
from aggregators.line_patterns import agg_assonance, agg_consonance, agg_alliteration
from aggregators.rhyme import agg_rhyme
from aggregators.rhythm import agg_syllable, agg_rhythm
from aggregators.characters_and_rhetoric import agg_similes, agg_character_count, agg_character_gender, \
    agg_character_num, agg_character_animation, agg_character_personification, agg_character_relations, \
    agg_character_relation_distribution
from aggregators.n_grams import agg_n_grams_by_line, agg_n_grams
from aggregators.semantics import agg_character_hypernyms, agg_modality_by_line, agg_polarity_by_line, \
    agg_subjectivity_by_line, agg_mood_by_line


def generalise(preset, plot):
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\analyse', preset + '.poems')), 'rb')
    poems = cPickle.load(f)
    f.close()

    template = Template(preset)

    aggregators = [agg_n_stanzas, agg_lines_per_stanza, agg_repeated_line_locations, agg_n_repeated_lines,
                   agg_n_distinct_sentences, agg_line_tenses, agg_overall_tense, agg_assonance, agg_consonance,
                   agg_alliteration, agg_rhyme, agg_syllable, agg_rhythm, agg_similes, agg_character_count,
                   agg_character_gender, agg_character_num, agg_character_animation, agg_character_personification,
                   agg_character_relations, agg_character_relation_distribution, agg_n_grams_by_line, agg_n_grams,
                   agg_character_hypernyms, agg_modality_by_line, agg_polarity_by_line, agg_subjectivity_by_line,
                   agg_mood_by_line]
    # Remove from list of aggregators according to parse args
    threads = []
    for aggregator in aggregators:
        thread = Thread(target=aggregator, args=(poems, template))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if plot:
        template.plot('')


def apply_givens(poems):
    pass
    #Take givens from builder/web interface/command line interface
    #givens = []
    #Run some list comprehensions in some nice way
    #for attr, value in givens:
        # For most cases:
    #    poems = [poem for poem in poems if value in getattr(poem, attr)]

    #return poems


def command_line_parser():
    arg_parser = argparse.ArgumentParser(description='Gather insight on poems.')

    arg_parser.add_argument('collection', choices=['test'], help='The particular collection of poems to be analysed.')

    arg_parser.add_argument('-plot', '--plot', action='store_true',
                            help='If true, shows a plot of every attribute. False by default.')

    arg_parser.add_argument('-persist', '--persist', action='store_true',
                            help='If true, serialise the results for later use. False by default.')

    #parser.add_argument('-nstanzas', type=int, choices=[1, 2, 3], help='Fix the number of stanzas in the poem')

    return arg_parser


