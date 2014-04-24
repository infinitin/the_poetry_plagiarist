__author__ = 'Nitin'
from aggregate import generalise
from shayar.poem_template import Template
# This import is required for the pickle load
# noinspection PyUnresolvedReferences,PyPep8Naming
import shayar.poem as poem
import os
import cPickle
import json

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


#Given the current set of applicable poems and the (new) givens, filter the poems accordingly.
#The keys of the givens correspond exactly to the attributes of the poem template object.
def apply_settings(ps, a, value):
    # Not quite but you get the point:
    if a == "n_stanzas":
        ps = [p for p in ps if value == p.stanzas]
    elif a == "lines_per_stanza":
        ps = [p for p in ps if value == p.lines]
    elif a == "repeated_line_locations":
        ps = [p for p in ps if set(value) == p.repeated_lines.values()]
    elif a == "n_repeated_lines":
        ps = [p for p in ps if value == len(p.repeated_lines.values())]
    elif a == "n_distinct_sentences":
        ps = [p for p in ps if value == p.distinct_sentences == value]
    elif a == "line_tenses":
        ps = [p for p in ps if value == p.tenses]
    elif a == "overall_tense":
        ps = [p for p in ps if value == p.tense]
    elif a == "assonance" or a == "consonance" or a == "alliteration":
        ps = [p for p in ps if value in [d.keys() for d in getattr(p, a)]]
    elif a == "rhyme":
        ps = [p for p in ps if tuple(value) in p.rhyme_scheme]
    elif a == "syllable":
        ps = [p for p in ps if tuple(value) in p.syllable_count]

    return ps


#Grab all the poems of a particular collection from store
def retrieve_all_poems(collection):
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\analyse', collection + '.poems')), 'rb')
    poems = cPickle.load(f)
    f.close()
    return poems

#Needs to be exactly as poem_template for this to work
json_input = '{"collection": "limericks", "plot": true, "persist": false}'
settings = json.loads(json_input)

aggregators = [agg_n_stanzas, agg_lines_per_stanza, agg_repeated_line_locations, agg_n_repeated_lines,
               agg_n_distinct_sentences, agg_line_tenses, agg_overall_tense, agg_assonance, agg_consonance,
               agg_alliteration, agg_rhyme, agg_syllable, agg_rhythm, agg_similes, agg_character_count,
               agg_character_gender, agg_character_num, agg_character_animation, agg_character_personification,
               agg_character_relations, agg_character_relation_distribution, agg_n_grams_by_line, agg_n_grams,
               agg_character_hypernyms, agg_modality_by_line, agg_polarity_by_line, agg_subjectivity_by_line,
               agg_mood_by_line]
possibles = globals().copy()
possibles.update(locals())

collection = settings["collection"]
poems = retrieve_all_poems(collection)
template = Template(collection)

# Set the value in the template
# Remove corresponding aggregators from list to execute
# Filter poems by this value as long as we still have some poems to work with
for attr in settings:
    if attr != "collection" and attr != "plot" and attr != "persist":
        setattr(template, attr, settings[attr])
        aggregators.remove(possibles.get('aggr_'+attr))
        filtered_poems = apply_settings(poems, attr, settings[attr])
        if filtered_poems:
            poems = filtered_poems

generalise(template, poems, aggregators, settings["plot"], settings["persist"])