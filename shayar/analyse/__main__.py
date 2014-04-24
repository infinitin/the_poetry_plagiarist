__author__ = 'Nitin'

import sys
import os
from shayar.poem import Poem
from detectors.utils import set_up_globals
import logging
from threading import Thread
import cPickle
import futures

logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)

from detectors import basic_structure, rhythm, line_pattern, rhyme, rhetoric, sentiment
from detectors.context import context


def analyse_poem(test):
    logging.info('Analysing' + str(test.poem))

    #logging.info('Counting number of stanzas')
    test.stanzas = basic_structure.count_stanzas(test.poem)

    #logging.info('Counting number of lines per stanza')
    test.lines = basic_structure.count_lines_per_stanza(test.poem)

    #logging.info('Finding and counting repeated lines')
    test.repeated_lines = basic_structure.count_repeated_lines(test.poem)

    #logging.info('Deciphering tenses of poem')
    test.tenses = basic_structure.detect_line_tense(test.poem)

    #logging.info('Compiling overall tense')
    test.overall_tense = basic_structure.detect_overall_tense(test.tenses)

    #logging.info('Counting distinct sentences')
    test.distinct_sentences = basic_structure.count_distinct_sentences(test.poem)

    #logging.info('Counting syllables in each line')
    test.syllable_count = rhythm.count_syllables(test.poem)

    #logging.info('Detecting instances of consonance')
    test.consonance = line_pattern.detect_consonance(test.poem)

    #logging.info('Detecting instances of assonance')
    test.assonance = line_pattern.detect_assonance(test.poem)

    #logging.info('Detecting instances of alliteration')
    test.alliteration = line_pattern.detect_alliteration(test.poem)

    #logging.info('Determining the rhyme scheme')
    test.rhyme_scheme = rhyme.determine_rhyme_scheme(test.poem)

    #logging.info('Detecting internal rhyme')
    test.internal_rhyme_scheme = rhyme.detect_internal_rhyme(test.poem)

    #logging.info('Listening to stress pattern')
    test.stress_pattern = rhythm.get_stress_pattern(test.poem)

    #logging.info('Looking out for similes')
    test.similes = rhetoric.detect_simile(test.poem)

    #logging.info("Determining speaker's point of view")
    test.point_of_view = basic_structure.determine_perspective(test.poem)

    #logging.info("Reading in-between the lines")
    test.characters = context.identify_characters_and_relationships(test.poem)

    #logging.info("Empathising")
    sentiment_tuples = sentiment.get_sentiment_by_line(test.poem)
    test.polarity_by_line = [round(polarity) for polarity, subjectivity in sentiment_tuples]
    test.subjectivity_by_line = [round(subjectivity) for polarity, subjectivity in sentiment_tuples]
    test.modality_by_line = sentiment.get_modality_by_line(test.poem)
    test.mood_by_line = sentiment.get_mood_by_line(test.poem)

    logging.info('Done' + str(test.poem))

import time
start = time.time()
poems = []
logging.info('Grabbing poems')
with open('limericks.txt', 'r') as f:
    buffer = []
    for line in f:
        if '~' in line:
            while not buffer[0].strip():
                buffer = buffer[1:]

            while not buffer[-1].strip():
                buffer = buffer[:-1]

            poems.append(Poem(map(str.strip, buffer)))
            buffer = []
        else:
            buffer.append(line)

#for filename in os.listdir(os.getcwd()):
#    if filename.endswith('.txt'):
#        f = open(filename)
#        poems.append(Poem(map(str.strip, f.readlines())))
#        f.close()

collection = 'limericks'
#logging.info('Setting up cmudict and other tools')
set_up_globals()

with futures.ThreadPoolExecutor(max_workers=10) as executor:
    future_to_poem = {executor.submit(analyse_poem, p): p for p in poems}

executor.shutdown()




#threads = []
#for p in poems[:10]:
#    thread = Thread(target=analyse_poem, args=(p,))
#    thread.start()
#    threads.append(thread)

#for thread in threads:
#    thread.join()

out = open(collection+'.poems', 'wb+')
out.truncate()
cPickle.dump(poems, out, -1)
out.close()

end = time.time()
print end - start