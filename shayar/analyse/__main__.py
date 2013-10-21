__author__ = 'Nitin'

from shayar.poem import Poem

from detectors import basic_structure, tense, rhythm, line_pattern, rhyme

#poetry_input = " The limerick packs laughs anatomical\nInto space that is quite economical.\n" \
#               "But the good ones I've seen\nSo seldom are clean\n" \
#               "And the clean ones so seldom are comical"

poetry_input = "From fairest creatures we desire increase,\nThat thereby beauty's rose might never die\n" \
               "But as the riper should by time decease,\nHis tender heir might bear his memory:\n" \
               "But thou contracted to thine own bright eyes,\nFeed'st thy light's flame with self-substantial fuel,\n" \
               "Making a famine where abundance lies,\nThy self thy foe, to thy sweet self too cruel:\n" \
               "Thou that art now the world's fresh ornament,\nAnd only heralsd to the gaudy spring,\n" \
               "Within thine own bud buriest thy content,\nAnd, tender churl, mak'st waste in niggarding:\n" \
               "  Pity the world, or else this glutton be,\n  To eat the world's due, by the grave and thee."

#poetry_input = "Glass boss\nMammals named Sam are clammy\nSlither Slather\nOn scrolls of silver snowy sentences"

limerick = Poem(poetry_input)
poem = limerick.poem

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

print str(limerick.poem) + "\n"

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