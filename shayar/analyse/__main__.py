__author__ = 'Nitin'

from shayar.poem import Poem

from detectors import basic_structure

poetry_input = " The limerick packs laughs anatomical\n Into space that is quite economical.\n" \
               "But the good ones I've seen\nSo seldom are clean\nAnd the clean ones so seldom are comical"

limerick = Poem(poetry_input)
limerick.stanzas = basic_structure.count_stanzas(limerick.poem)
limerick.lines = basic_structure.count_lines_per_stanza(limerick.poem)

print str(limerick.poem) + "\n"

print "A limerick has " + str(limerick.stanzas) + " stanza(s) "
print "with a total of " + str(sum(limerick.lines)) + " lines "
print "in the format of " + str(limerick.lines) + "."