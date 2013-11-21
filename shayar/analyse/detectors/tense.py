__author__ = 'Nitin'

import re
from pattern.text.en import tag, tenses
from collections import Counter


# First grab all the verbs in the line
# Then we get the tenses of all the verbs and just take the first element, i.e. past, present, future
#  We ignore the rest of the tense output (imperative, perfect, imperfect etc.) because it is not important for
#  generalisation or analysis, and is not totally accurate.
def detect_line_tense(poem):
    poem_verb_set = []
    for line in poem:
        line_verb = ""
        if "'" in line:
            line = __replace_contractions(line)
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


# Replace known abbreviations with the full form so that it gets picked up by cmudict.
# Can be removed by simply extending the cmudict.
def __replace_contractions(line):
    replacement_patterns = [(r'won\'t', 'will not'),
                            (r'can\'t', 'cannot'),
                            (r'i\'m', 'i am'),
                            (r'ain\'t', 'is not'),
                            (r'(\w+)\'ll', '\g<1> will'),
                            (r'(\w+)n\'t', '\g<1> not'),
                            (r'(\w+)\'ve', '\g<1> have'),
                            (r'(\w+t)\'s', '\g<1> is'),
                            (r'(\w+)\'re', '\g<1> are'),
                            (r'(\w+)\'d', '\g<1> would')]
    expanded_line = line
    patterns = [(re.compile(regex), expansion) for (regex, expansion) in replacement_patterns]
    for (pattern, expansion) in patterns:
        (expanded_line, count) = re.subn(pattern, expansion, expanded_line)
    return expanded_line