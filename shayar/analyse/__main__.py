__author__ = 'Nitin'

from shayar.poem import Poem

from detectors import basic_structure, tense, rhythm, line_pattern

poetry_input = " The limerick packs laughs anatomical\nInto space that is quite economical.\n" \
               "But the good ones I've seen\nSo seldom are clean\n" \
               "And the clean ones so seldom are comical"

#poetry_input = "Glass boss\nMammals named Sam are clammy\nSlither Slather"

limerick = Poem(poetry_input)
limerick.stanzas = basic_structure.count_stanzas(limerick.poem)
limerick.lines = basic_structure.count_lines_per_stanza(limerick.poem)
limerick.repeated_lines = basic_structure.count_repeated_lines(limerick.poem)
limerick.tense = tense.detect_line_tense(limerick.poem)
limerick.syllable_count = rhythm.count_syllables(limerick.poem)
limerick.consonance = line_pattern.detect_consonance(limerick.poem)
limerick.assonance = line_pattern.detect_assonance(limerick.poem)

print str(limerick.poem) + "\n"

print "A limerick has " + str(limerick.stanzas) + " stanza(s) "
print "with a total of " + str(sum(limerick.lines)) + " lines "
print "in the format of " + str(limerick.lines) + "."
print str(len(limerick.repeated_lines)) + " line(s) are repeated in this poem"
print "at positions " + str(limerick.repeated_lines.values()) + "."
print "The tenses of the lines in the given limerick are " + str(limerick.tense)
print "Giving it a " + str(tense.detect_overall_tense(limerick.tense)) + " tense overall."
print "The syllable lengths of each line are as follows: " + str(limerick.syllable_count) + "."
print "The poem has consonance scores of: " + str(limerick.consonance)
print "and assonance scores of: " + str(limerick.assonance)