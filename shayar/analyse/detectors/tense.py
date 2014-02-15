__author__ = 'Nitin'

from pattern.text.en import tag, tenses
from collections import Counter
from utils import replace_contractions


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