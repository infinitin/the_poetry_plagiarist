__author__ = 'Nitin'
from utils import get_most_common
import re


def agg_syllable(poems, template):
    template.syllable_patterns = [tuple(poem.syllable_count) for poem in poems]


def agg_rhythm(poems, template):
    stress_patterns = []

    max_num_lines = max([len(poem.stress_pattern) for poem in poems])
    rhythm_possibilities_by_line = []
    for line in range(0, max_num_lines):
        line_rhythm_possibilities = []
        for poem in poems:
            if line < len(poem.stress_pattern):
                line_rhythm_possibilities.append(poem.stress_pattern[line])
        rhythm_possibilities_by_line.append(line_rhythm_possibilities)

    for line_rhythm_possibilities in rhythm_possibilities_by_line:
        line_stress_patterns = []
        while line_rhythm_possibilities:
            possibilities = [rhythm for line_rhythm_possibility in line_rhythm_possibilities
                             for rhythm in line_rhythm_possibility]
            most_commons = get_most_common(possibilities)
            most_common = get_best(most_commons)
            line_stress_patterns.extend([possibility for possibility in possibilities if possibility == most_common])
            line_rhythm_possibilities = [rhythm_possibility for rhythm_possibility in line_rhythm_possibilities
                                         if most_common not in rhythm_possibility]

        stress_patterns.append(line_stress_patterns)

    template.stress_patterns = stress_patterns


def get_best(most_commons):
    r = re.compile(r"(.+?)(?=\1)")
    try:
        num_max_repeated_substrings = [pattern.count(r.findall(pattern)[0]) for pattern in most_commons]
        index_of_most_common = num_max_repeated_substrings.index(max(num_max_repeated_substrings))
        return most_commons[index_of_most_common]
    except IndexError:
        return most_commons[0]
