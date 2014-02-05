__author__ = 'Nitin'


negative_adverbs = set(['not', 'seldom', 'hardly', 'barely', 'scarcely', 'rarely'])
negative_r_and_dts = set(['not', 'seldom', 'hardly', 'barely', 'scarcely', 'rarely', 'no', 'neither'])


def check_for_of(sentence, index_of_noun):
    n = 0
    if sentence[index_of_noun + 1].string == 'of' or sentence[index_of_noun + 1].string == 'o':
        n = 2
        while not sentence[index_of_noun + n].type.startswith('N'):
            n += 1


    return n