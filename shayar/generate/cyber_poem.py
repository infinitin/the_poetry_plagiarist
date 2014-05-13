__author__ = 'Nitin'
from shayar.poem import Poem


class CyberPoem(Poem):

    phrases = {}    # Will hold the NLG elements

    def __init__(self):
        Poem.__init__(self, [])