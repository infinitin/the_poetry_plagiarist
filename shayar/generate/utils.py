__author__ = 'Nitin'
import random
from collections import Counter

num_poems = 0


def select(options):
    # if one value covers more than 50% and is at least 3x the next highest value, treat it as unambiguous
    two_most_popular = Counter(options).most_common(2)
    if len(two_most_popular) == 1 or (two_most_popular[0][1] >= len(options)/2 and two_most_popular[1][1] <= two_most_popular[0][1]/3):
        return two_most_popular[0][0]
    else:
        return random.choice(options)