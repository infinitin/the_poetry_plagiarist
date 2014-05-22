__author__ = 'Nitin'
from shayar.poem import Poem
import builder
from builder import make_clause


class CyberPoem(Poem):

    phrases = []    # Will hold the phrase elements

    def __init__(self):
        Poem.__init__(self, [])

    def realise(self):
        # FIXME: Make work with stanzas
        for l in range(0, sum(self.lines)):
            self.poem.append(str(builder.realiser.realise(make_clause(self.phrases[l])).getRealisation()))

        for line in self.poem:
            print line


