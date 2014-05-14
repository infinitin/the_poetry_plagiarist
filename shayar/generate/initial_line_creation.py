from __future__ import division

__author__ = 'Nitin'
import utils
from random import random
from collections import Counter
from shayar.generalise.aggregators.rhythm import agg_rhythm
from pattern.text.en import lemma
from builder import build_poem_line


def create_initial_line(new_poem, template, poems, init_line_index):
    chosen_ngram = select_n_gram(template, init_line_index)
    if chosen_ngram:
        poems = [p for p in poems if set(chosen_ngram.split(' ')).issubset([lemma(word) for word in p.poem[init_line_index].split(' ')])]
        agg_rhythm(poems, template)

    #TODO: send to big builder
    new_poem.phrases[init_line_index] = build_poem_line(new_poem, template, poems, init_line_index)

    #TODO: Rephrase to fit to streess peetteerrns

    #TODO: Save the final stress pattern in the template at this init index



def select_n_gram(template, init_line_index):
    options = template.n_grams_by_line[init_line_index]
    two_most_popular = Counter(options).most_common(2)
    if len(two_most_popular) == 1 or (two_most_popular[0][1] >= len(options)/2 and two_most_popular[1][1] <= two_most_popular[0][1]/3):
        return two_most_popular[0][0]
    else:
        chosen_ngram = ''
        for ngram in options:
            chance = random()
            if chance < ngram[1]/utils.num_poems:
                chosen_ngram = ngram[0]
                break

    return chosen_ngram

