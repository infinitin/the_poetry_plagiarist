__author__ = 'Nitin'
import random
from collections import Counter

num_poems = 0


def select(options):
    # reject those that are 3x less than the most common
    counts = Counter(options)
    most_common = counts.most_common()[0][1]
    remaining_options = [count for count in counts.keys() if (counts[count] * 3) > most_common]
    return random.choice(remaining_options)


