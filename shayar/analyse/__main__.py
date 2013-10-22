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

poem = line_patterns.poem

limerick.stanzas = basic_structure.count_stanzas(poem)
limerick.lines = basic_structure.count_lines_per_stanza(poem)
limerick.repeated_lines = basic_structure.count_repeated_lines(poem)
limerick.tense = tense.detect_line_tense(poem)
limerick.syllable_count = rhythm.count_syllables(poem)
limerick.consonance = line_pattern.detect_consonance(poem)
limerick.assonance = line_pattern.detect_assonance(poem)
limerick.alliteration = line_pattern.detect_alliteration(poem)
limerick.rhyme_scheme = rhyme.determine_rhyme_scheme(poem)
limerick.internal_rhyme_scheme = rhyme.detect_internal_rhyme(poem)
limerick.stress_pattern = rhythm.get_stress_pattern(poem)

print "A limerick has " + str(limerick.stanzas) + " stanza(s) "
print "with a total of " + str(sum(limerick.lines)) + " lines "
print "in the format of " + str(limerick.lines) + "."
print str(len(limerick.repeated_lines)) + " line(s) are repeated in this poem"
print "at positions " + str(limerick.repeated_lines.values()) + "."
print "The tenses of the lines in the given limerick are " + str(limerick.tense) + ","
print "giving it a " + str(tense.detect_overall_tense(limerick.tense)) + " tense overall."
print "The syllable lengths of each line are as follows: " + str(limerick.syllable_count) + "."
print "The poem has consonance scores of: " + str(limerick.consonance) + ","
print "assonance scores of: " + str(limerick.assonance)
print "and alliteration scores of " + str(limerick.alliteration)
print "The rhyme scheme is " + str(limerick.rhyme_scheme) + "."
print "There is also internal rhyme: " + str(limerick.internal_rhyme_scheme) + "."
print "The stress patterns of each of the lines is: " + str(limerick.stress_pattern) + "."