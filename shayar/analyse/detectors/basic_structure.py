__author__ = 'Nitin'

from pattern.text.en import parsetree, tag, tenses
from collections import Counter
from utils import replace_contractions


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
    non_unique_lines = [x for x, y in Counter(poem).items() if y > 1]
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


# First grab all the verbs in the line
# Then we get the tenses of all the verbs and just take the first element, i.e. past, present, future
#  We ignore the rest of the tense output (imperative, perfect, imperfect etc.) because it is not important for
#  generalisation or analysis, and is not totally accurate.
def detect_line_tense(poem):
    poem_verb_set = []
    for line in poem:
        line_verb = ""
        if "'" in line:
            line = replace_contractions(line)
        for word, t in tag(line, tokenize=True):
            if t.startswith("V"):
                line_verb = str(word)
        poem_verb_set.append(line_verb)

    line_tenses = []
    for line_verb in poem_verb_set:
        if not line_verb:
            continue
        possible_tenses = []
        for tense in tenses(line_verb):
            possible_tenses.append(tense[0])
        try:
            line_tenses.append(detect_overall_tense(possible_tenses))
        except IndexError:
            line_tenses.append('')

    return line_tenses


# We take the mode of the tenses in a line as the overall tense.
def detect_overall_tense(line_tenses):
    return [x for x, y in Counter(line_tenses).most_common()][0]