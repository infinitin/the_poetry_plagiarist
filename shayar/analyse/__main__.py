__author__ = 'Nitin'

import sys
import os
from shayar.poem import Poem
from detectors.utils import set_up_globals
import logging
import threading
import cPickle

logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)

from detectors import basic_structure, rhythm, line_pattern, rhyme, rhetoric
from detectors.context import context


def analyse_poem(test):
    logging.info('Analysing' + str(test.poem))

    logging.info('Counting number of stanzas')
    test.stanzas = basic_structure.count_stanzas(test.poem)

    logging.info('Counting number of lines per stanza')
    test.lines = basic_structure.count_lines_per_stanza(test.poem)

    logging.info('Finding and counting repeated lines')
    test.repeated_lines = basic_structure.count_repeated_lines(test.poem)

    logging.info('Deciphering tenses of poem')
    test.tenses = basic_structure.detect_line_tense(test.poem)

    logging.info('Compiling overall tense')
    test.overall_tense = basic_structure.detect_overall_tense(test.tenses)

    logging.info('Counting syllables in each line')
    test.syllable_count = rhythm.count_syllables(test.poem)

    logging.info('Detecting instances of consonance')
    test.consonance = line_pattern.detect_consonance(test.poem)

    logging.info('Detecting instances of assonance')
    test.assonance = line_pattern.detect_assonance(test.poem)

    logging.info('Detecting instances of alliteration')
    test.alliteration = line_pattern.detect_alliteration(test.poem)

    logging.info('Determining the rhyme scheme')
    test.rhyme_scheme = rhyme.determine_rhyme_scheme(test.poem)

    logging.info('Detecting internal rhyme')
    test.internal_rhyme_scheme = rhyme.detect_internal_rhyme(test.poem)

    logging.info('Listening to stress pattern')
    test.stress_pattern = rhythm.get_stress_pattern(test.poem)

    logging.info('Looking out for similes')
    test.similes = rhetoric.detect_simile(test.poem)

    logging.info("Determining speaker's point of view")
    test.point_of_view = basic_structure.determine_perspective(test.poem)

    logging.info("Reading in-between the lines")
    test.characters = context.identify_characters_and_relationships(test.poem)

    logging.info('Done' + str(test.poem))


class AnalysisEngine(threading.Thread):

    def __init__(self, poem):
        threading.Thread.__init__(self)
        self.poem = poem

    def run(self):
        analyse_poem(self.poem)
        return self.poem


poems = []
logging.info('Grabbing poems')
for filename in os.listdir(os.getcwd()):
    if filename.endswith('.txt'):
        f = open(filename)
        poems.append(Poem(map(str.strip, f.readlines())))
        f.close()

collection = sys.argv[1]
logging.info('Setting up cmudict and other tools')
set_up_globals()
analysed_poems = []
threads = []
for poem in poems:
    thread = AnalysisEngine(poem)
    analysed_poem = thread.start()
    analysed_poems.append(analysed_poem)
    threads.append(thread)

for thread in threads:
    thread.join()

out = open(collection+'.poems', 'w+')
cPickle.dump(analysed_poems, out, -1)
out.close()