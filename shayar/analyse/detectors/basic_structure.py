__author__ = 'Nitin'


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