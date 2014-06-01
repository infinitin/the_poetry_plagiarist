__author__ = 'Nitin'
from pattern.db import CSV
import logging


def get_knowledge_from_associations(g):
    logging.info('Gathering knowledge from associations')
    data = 'C:\\Python27\\associations_data\\all.csv'
    data = CSV.load(data)
    adjectives = ['A', 'ADJ', 'AJ']
    adverbs = ['AD', 'ADV', 'AV']
    for concept1, concept2, pos1, pos2 in data:
        #FIXME: Try to figure it out if no pos is given
        pos1 = pos1.strip()
        pos2 = pos2.strip()
        if not pos1 or not pos2 or pos1 == 'C' or pos2 == 'C':
            continue

        if pos1.startswith('N') and pos2 in adjectives:
            g.append(tuple([concept1.lower() + '.n', concept2.lower() + '.a', 'HasProperty']))
            continue
        elif pos1.startswith('V') and pos2 in adverbs:
            g.append(tuple([concept1.lower() + '.v', concept2.lower() + '.adv', 'HasProperty']))
            continue
        elif pos1 in adjectives and pos2.startswith('N'):
            g.append(tuple([concept2.lower() + '.n', concept1.lower() + '.a', 'HasProperty']))
            continue
        elif pos1 in adverbs and pos2.startswith('V'):
            g.append(tuple([concept2.lower() + '.v', concept1.lower() + '.adv', 'HasProperty']))
            continue

        if pos1 not in adverbs and pos2 not in adverbs:
            g.append(tuple(
                [concept1.lower() + '.' + pos1[0].lower(), concept2.lower() + '.' + pos2[0].lower(),
                 'RelatedTo']))