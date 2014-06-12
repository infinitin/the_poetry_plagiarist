__author__ = 'Nitin'
from aggregate import generalise
from shayar.poem_template import Template
# This import is required for the pickle load
# noinspection PyUnresolvedReferences,PyPep8Naming
import shayar.poem as poem
from utils import apply_settings, retrieve_all_poems
import json
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)

from aggregators.basic_structure import agg_n_stanzas, agg_lines_per_stanza, agg_repeated_line_locations, \
    agg_n_repeated_lines, agg_n_distinct_sentences, agg_line_tenses, agg_overall_tense, agg_perspective
from aggregators.line_patterns import agg_assonance, agg_consonance, agg_alliteration
from aggregators.rhyme import agg_rhyme
from aggregators.rhythm import agg_syllable, agg_rhythm
from aggregators.characters_and_rhetoric import agg_similes, agg_character_count, agg_character_gender, \
    agg_character_num, agg_character_animation, agg_character_personification, agg_character_relations, \
    agg_character_relation_distribution
from aggregators.n_grams import agg_n_grams_by_line, agg_n_grams
from aggregators.semantics import agg_hypernym_ancestors, agg_modality_by_line, agg_polarity_by_line, \
    agg_subjectivity_by_line, agg_mood_by_line

#Needs to be exactly as poem_template for this to work
json_input = '{"collection": "sonnets1", "plot": true, "persist": true}'
settings = json.loads(json_input)

aggregators = [agg_n_stanzas, agg_lines_per_stanza, agg_repeated_line_locations, agg_n_repeated_lines,
               agg_n_distinct_sentences, agg_line_tenses, agg_overall_tense, agg_perspective, agg_assonance, agg_consonance,
               agg_alliteration, agg_rhyme, agg_syllable, agg_rhythm, agg_similes, agg_character_count,
               agg_character_gender, agg_character_num, agg_character_animation, agg_character_personification,
               agg_character_relations, agg_character_relation_distribution, agg_n_grams_by_line, agg_n_grams,
               agg_hypernym_ancestors, agg_modality_by_line, agg_polarity_by_line, agg_subjectivity_by_line,
               agg_mood_by_line]
possibles = globals().copy()
possibles.update(locals())

collection = settings["collection"]
poems = retrieve_all_poems(collection)
template = Template(collection)

# Set the value in the template
# Remove corresponding aggregators from list to execute
# Filter poems by this value as long as we still have some poems to work with
for attr in settings.keys():
    if attr != "collection" and attr != "plot" and attr != "persist":
        setattr(template, attr, settings[attr])
        aggregators.remove(possibles.get('aggr_'+attr))
        filtered_poems = apply_settings(poems, attr, settings[attr])
        if filtered_poems:
            poems = filtered_poems

generalise(template, poems, aggregators, settings["plot"], settings["persist"])