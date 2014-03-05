__author__ = 'Nitin'
from collections import Counter, defaultdict


def agg_assonance(poems, template):
    template.assonance = aggregate(poems, 'assonance')


def agg_consonance(poems, template):
    template.consonance = aggregate(poems, 'consonance')


def agg_alliteration(poems, template):
    template.alliteration = aggregate(poems, 'alliteration')


def aggregate(poems, attribute):
    pattern_dict = defaultdict(list)
    per_poem_pattern = []
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








