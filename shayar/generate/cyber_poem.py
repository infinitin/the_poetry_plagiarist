__author__ = 'Nitin'
from shayar.poem import Poem


class CyberPoem(Poem):

    phrases = {}    # Will hold the NLG elements

    def __init__(self):
        Poem.__init__(self, [])

    def realise(self):
        pass
        #FIXME: Make this work for stanzas
        #for phrase_num in range(0, len(phrases)):
            #line = realiser.realise(phrases[phrase_num]).getRealisation()
            #self.poem.append(line)
            #print line