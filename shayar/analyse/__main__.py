__author__ = 'Nitin'

from shayar.poem import Poem

from detectors import basic_structure, tense, rhythm, line_pattern, rhyme

f = open("limerick.txt")
limerick = Poem(map(str.strip, f.readlines()))
f = open("sonnet.txt")
sonnet = Poem(map(str.strip, f.readlines()))
f = open("line patterns.txt")
line_patterns = Poem(map(str.strip, f.readlines()))
f = open("haiku.txt")
haiku = Poem(map(str.strip, f.readlines()))
f.close()

test = line_patterns

test.stanzas = basic_structure.count_stanzas(test.poem)
test.lines = basic_structure.count_lines_per_stanza(test.poem)
test.repeated_lines = basic_structure.count_repeated_lines(test.poem)
test.tenses = tense.detect_line_tense(test.poem)
test.overall_tense = tense.detect_overall_tense(test.tenses)
test.syllable_count = rhythm.count_syllables(test.poem)
test.consonance = line_pattern.detect_consonance(test.poem)
test.assonance = line_pattern.detect_assonance(test.poem)
test.alliteration = line_pattern.detect_alliteration(test.poem)
test.rhyme_scheme = rhyme.determine_rhyme_scheme(test.poem)
test.internal_rhyme_scheme = rhyme.detect_internal_rhyme(test.poem)
test.stress_pattern = rhythm.get_stress_pattern(test.poem)

print str(test)