from __future__ import division

__author__ = 'Nitin'
from utils import select
import utils
from random import random, choice


def init_poem(new_poem, template):
    new_poem.perspective = select(template.perspective)
    template.perspective = [new_poem.perspective]

    new_poem.overall_tense = select(template.overall_tense)
    template.overall_tense = new_poem.overall_tense

    new_poem.stanzas = select(template.stanzas)
    template.stanzas = [new_poem.stanzas]

    new_poem.lines = select([num_lines for num_lines in template.num_lines if len(num_lines) == new_poem.stanzas])
    template.num_lines = [new_poem.lines]

    new_poem.repeated_lines = select_rl(template.repeated_lines_locations, sum(new_poem.lines))
    template.repeated_lines_locations = [new_poem.repeated_lines]

    new_poem.rhyme_scheme = select([rs for rs in template.rhyme_schemes if len(rs) == sum(new_poem.lines)])
    template.rhyme_schemes = [new_poem.rhyme_scheme]

    #Choose the everything for the whole poem straight up. May want to make this more specific as per first line later.
    for l in range(0, sum(new_poem.lines)):
        template.stress_patterns[l] = choice(template.stress_patterns[l])
        template.n_grams_by_line[l] = select_n_gram(template, l)


def select_rl(options, max_lines):
    return []
    filtered_rl = []
    for repeated_lines in options:
        if repeated_lines:
            if max(repeated_lines) < sum(max_lines):
                filtered_rl.append(repeated_lines)

    return filtered_rl


def select_n_gram(template, init_line_index):
    options = template.n_grams_by_line[init_line_index]
    chosen_ngram = ''
    for ngram in options:
        chance = random()
        if chance < (ngram[1] / utils.num_poems):
            chosen_ngram = ngram[0]
            break

    return chosen_ngram