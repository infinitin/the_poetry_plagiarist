__author__ = 'Nitin'

from shayar.poem import Poem
from detectors.utils import set_up_globals
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)

from detectors import basic_structure, rhythm, line_pattern, rhyme, rhetoric
from detectors.context import context

logging.info('Grabbing poems')
f = open("limerick.txt")
limerick = Poem(map(str.strip, f.readlines()))
f = open("sonnet.txt")
sonnet = Poem(map(str.strip, f.readlines()))
f = open("line patterns.txt")
line_patterns = Poem(map(str.strip, f.readlines()))
f = open("haiku.txt")
haiku = Poem(map(str.strip, f.readlines()))
f = open("similes.txt")
similes = Poem(map(str.strip, f.readlines()))
f = open("simple.txt")
simple = Poem(map(str.strip, f.readlines()))
f.close()

logging.info('Begin analysis')
test = limerick

logging.info('Setting up cmudict and other tools')
set_up_globals()

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

logging.info('Listening for onomatopoeia')
test.onomatopoeia = rhetoric.identify_onomatopoeia(test.poem)

logging.info("Determining speaker's point of view")
test.point_of_view = basic_structure.determine_perspective(test.poem)

logging.info("Reading in-between the lines")
test.characters = context.identify_characters_and_relationships(test.poem)

print str(test)