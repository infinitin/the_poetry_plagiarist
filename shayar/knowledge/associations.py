__author__ = 'Nitin'
from pattern.db import CSV
import logging


def get_knowledge_from_associations():
    logging.info('Gathering knowledge from associations')
    g = []
    data = 'C:\\Python27\\associations_data\\all.csv'
    data = CSV.load(data)
    adjectives = ['A', 'ADJ', 'AJ']
    adverbs = ['AD', 'ADV', 'AV']
    for concept1, concept2, pos1, pos2 in data:
        if pos1 == 'C' or pos2 == 'C':
            continue

        if pos1.startswith('N') and pos2 in adjectives:
            g.append(tuple([concept1 + '.n', concept2 + '.a', 'HasProperty']))
            continue
        elif pos1.startswith('V') and pos2 in adverbs:
            g.append(tuple([concept1 + '.v', concept2 + '.adv', 'HasProperty']))
            continue
        elif pos1 in adjectives and pos2.startswith('N'):
            g.append(tuple([concept2 + '.n', concept1 + '.a', 'HasProperty']))
            continue
        elif pos1 in adverbs and pos2.startswith('V'):
            g.append(tuple([concept2 + '.v', concept1 + '.adv', 'HasProperty']))
            continue

        if pos1 not in adverbs and pos2 not in adverbs:
            g.append(tuple([concept1 + '.' + pos1[0].lower(), concept2 + pos2[0].lower(), 'RelatedTo']))

    return g