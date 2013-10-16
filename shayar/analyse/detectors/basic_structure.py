__author__ = 'Nitin'

import collections

def count_stanzas(poem):
    if not poem:
        return 0

    stanzas = 1
    for line in poem:
        if line.isspace():
            stanzas += 1
    return stanzas


def count_lines_per_stanza(poem):
    lines_per_stanza = []

    lines = 0
    for line in poem:
        if line.isspace():
            lines_per_stanza.append(lines)
            lines = 0
        else:
            lines += 1

    lines_per_stanza.append(lines)

    return lines_per_stanza


def count_repeated_lines(poem):
    non_unique_lines = [x for x, y in collections.Counter(poem).items() if y > 1]
    if not non_unique_lines:
        return {}

    repeated_lines = {}
    for line in non_unique_lines:
        repeated_lines[line] = [i for i, x in enumerate(poem) if x == line]

    return repeated_lines


