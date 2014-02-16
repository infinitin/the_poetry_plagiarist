__author__ = 'Nitin'

import collections
from pattern.text.en import parsetree


def count_stanzas(poem):
    return poem.count('') + 1


def count_lines_per_stanza(poem):
    lines_per_stanza = []

    lines = 0
    for line in poem:
        if not line.strip():
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


def count_distinct_sentences(poem):
    lines = ""
    for line in poem:
        lines += line.lower() + " "

    return len(parsetree(lines))


def determine_perspective(poem):
    altogether = ''
    for line in poem:
        altogether += line + ' '

    words = set(altogether.split(' '))

    first_person_words = {'i', 'me', 'my', 'myself', 'mine'}
    second_person_words = {'you', 'your', 'yourself', 'yours', 'thy', 'thine', 'thou', 'thee'}

    first_person = list(first_person_words & words)
    second_person = list(second_person_words & words)

    if first_person or second_person:
        if len(first_person) >= len(second_person):
            return "first"
        else:
            return "second"
    else:
        return "third"