__author__ = 'Nitin'
import random
from shayar.poem import Poem
from collections import Counter


def init_poem(template):
    new_poem = Poem([])

    new_poem.perspective = select(template.perspective)
    new_poem.tenses = select(template.overall_tense)
    new_poem.stanzas = select(template.stanzas)
    new_poem.lines = select(num_lines for num_lines in template.num_lines if len(num_lines) == new_poem.stanzas)

    new_poem.repeated_lines = select_rl(template.repeated_lines_locations, sum(new_poem.lines))

    return new_poem


def select(options):
    # if one value covers more than 50% and is at least 3x the next highest value, treat it as unambiguous
    two_most_popular = Counter(options).most_common(2)
    if len(two_most_popular) == 1 or (two_most_popular[0][1] >= len(options)/2 and two_most_popular[1][1] <= two_most_popular[0][1]/3):
        return two_most_popular[0][0]
    else:
        return random.choice(options)


def select_rl(options, max_lines):
    filtered_rl = []
    for repeated_lines in options:
        if repeated_lines:
            if max(repeated_lines) < sum(max_lines):
                filtered_rl.append(repeated_lines)

    return filtered_rl