__author__ = 'Nitin'
from collections import Counter, defaultdict
import logging


def agg_assonance(poems, template):
    logging.info('Starting aggregator: agg_assonance')
    template.assonance = aggregate(poems, 'assonance')
    logging.info('Aggregator finished: agg_assonance')


def agg_consonance(poems, template):
    logging.info('Starting aggregator: agg_consonance')
    template.consonance = aggregate(poems, 'consonance')
    logging.info('Aggregator finished: agg_consonance')


def agg_alliteration(poems, template):
    logging.info('Starting aggregator: agg_alliteration')
    template.alliteration = aggregate(poems, 'alliteration')
    logging.info('Aggregator finished: agg_alliteration')


def aggregate(poems, attribute):
    # Dictionary whose values are lists
    pattern_dict = defaultdict(list)
    per_poem_pattern = []
    # Get the
    for poem in poems:
        line_pattern = Counter({})
        line_pattern_dicts = getattr(poem, attribute)

        for line_pattern_dict in line_pattern_dicts:
            line_pattern += Counter(line_pattern_dict)

        per_poem_pattern.append(line_pattern)

    for poem_pattern in per_poem_pattern:
        for k in poem_pattern.keys():
            pattern_dict[k].append(poem_pattern[k])

    return pattern_dict








