__author__ = 'Nitin'
import random
from shayar.poem import Poem
from collections import Counter


def init_poem(settings):
    new_poem = Poem([])
    num_poems = len(settings["stanzas"])

    new_poem.stanzas = select(settings["stanzas"])
    new_poem.lines = select(settings["num_lines"])     # depends on the number of stanzas
    new_poem.repeated_lines = select(settings["repeated_lines_locations"])
    new_poem.perspective = select(settings["perspective"])
    new_poem.tenses = select(settings["overall_tense"])


def select(options):
    # if one value covers more than 50% and is at least 3x the next highest value, treat it as unambiguous
    two_most_popular = Counter(options).most_common(2)
    if two_most_popular[0][1] >= len(options)/2 and two_most_popular[1][1] <= two_most_popular[0][1]/3:
        return two_most_popular[0][0]
    else:
        return random.choice(options)