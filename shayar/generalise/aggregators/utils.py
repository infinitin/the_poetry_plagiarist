__author__ = 'Nitin'
from collections import Counter
import logging


def get_most_common(list):
    if not list:
        return []

    count = Counter(list)
    max_count = count.most_common()[0][1]

    return [item for item in list if list.count(item) == max_count]
