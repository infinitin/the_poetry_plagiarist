__author__ = 'Nitin'
# This import is required for the pickle load
# noinspection PyUnresolvedReferences,PyPep8Naming
from shayar.poem_template import Template
import os
import cPickle
import json
from initialisation import init_poem
from cyber_poem import CyberPoem
from shayar.generalise.utils import retrieve_all_poems, apply_settings
import utils
from initial_line_creation import create_initial_line
from shayar.generalise.aggregators import rhythm, rhyme
from collections import Counter
from builder import boot_builder, shutdown_builder

import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)


#Grab the poem template of a particular collection from store
def retrieve_template(collection):
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\generalise', collection + '.template')), 'rb')
    stored_template = cPickle.load(f)
    f.close()
    return stored_template

#Input from user
json_input = '{"collection": "limericks"}'
settings = json.loads(json_input)
collection = settings["collection"]

#Get template, poems from store
template = retrieve_template(collection)
poems = retrieve_all_poems(collection)
utils.num_poems = len(poems)

#Init poem
new_poem = CyberPoem()
# A bit weird to be returning the poems list here, but it seems to be passed by value for some reason
init_poem(new_poem, template, poems)

#Build the first line (change the last parameter in future to build a different line first.
# Useful if a line is given by the user or if we choose the one with the most n_grams.
init_line_index = 0
create_initial_line(new_poem, template, poems, init_line_index)

#FIXME: TEST THIS STUFF
#Choose stress patterns and rhyme scheme of rest of the lines
#If there is an unambiguous rhyme scheme, use that
options = template.rhyme_schemes
two_most_popular = Counter(options).most_common(2)
if len(two_most_popular) == 1 or (two_most_popular[0][1] >= len(options)/2 and two_most_popular[1][1] <= two_most_popular[0][1]/3):
    new_poem.rhyme_scheme = two_most_popular[0][0]
    template.rhyme_schemes = [new_poem.rhyme_scheme]

#Otherwise filter the poems down to those with this chosen stress pattern for this chosen line and choose again
poems = apply_settings(poems, 'stress_patterns', template.stress_patterns[init_line_index])
if not new_poem.rhyme_scheme:
    rhyme.agg_rhyme(poems, template)
    new_poem.rhyme_scheme = utils.select(template.rhyme_schemes)

#And choose the stress patterns for the rest of the poem
rhythm.agg_rhythm(poems, template)
for line_index in range(0, sum(new_poem.lines)):
    if line_index != init_line_index:
        new_poem.stress_pattern[line_index] = utils.select(template.stress_patterns[line_index])


#TODO: Build the rest of the lines, checking for rhyme scheme, ngrams, rhyme etc. etc.
#TODO: Don't forget the persona creation module
#TODO: Also gotta make distinct sentences without losing stress patterns


#Realise poem into the CyberPoem.poem attribute and return to user
CyberPoem.realise()

shutdown_builder()