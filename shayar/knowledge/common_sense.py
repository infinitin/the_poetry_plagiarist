__author__ = 'Nitin'
from pattern.db import CSV
import logging


def get_knowledge_from_pattern_common_sense(g):
    logging.info('Gathering knowledge from pattern common sense relations')
    temp = []
    data = 'C:\\Python27\\Lib\\site-packages\\pattern\\graph\\commonsense.csv'
    data = CSV.load(data)
    for concept1, relation, concept2, context, weight in data:
        if relation == 'is-a':
            g.append(tuple([concept1+'.n', concept2+'.n', 'IsA']))
        elif relation == 'is-part-of':
            g.append(tuple([concept1+'.n', concept2+'.n', 'PartOf']))
        elif relation == 'is-property-of':
            g.append(tuple([concept2+'.n', concept1+'.a', 'HasProperty']))

        elif relation == 'is-opposite-of':
            temp.append(tuple([concept1, concept2, 'NotRelatedTo']))
        elif relation == 'is-related-to':
            temp.append(tuple([concept1, concept2, 'RelatedTo']))
        elif relation == 'is-same-as':
            temp.append(tuple([concept1, concept2, 'RelatedTo']))
        elif relation == 'is-effect-of':
            temp.append(tuple([concept1, concept2, 'RelatedTo']))

        if context == 'people':
            g.append(tuple([concept1+'.n', 'person', 'IsA']))

    logging.info('Cleaning up...')
    concepts = set([head for head, tail, relation in g] + [tail for head, tail, relation in g])
    for chance in temp:
        concept1 = chance[0]
        concept2 = chance[1]

        if concept1+'.n' in concepts:
            concept1 += '.n'
        elif concept1+'.v' in concepts:
            concept1 += '.v'
        elif concept1+'.a' in concepts:
            concept1 += '.a'
        elif concept1+'.adv' in concepts:
            concept1 += '.adv'
        else:
            continue

        if concept2+'.n' in concepts:
            concept2 += '.n'
        elif concept2+'.v' in concepts:
            concept2 += '.v'
        elif concept2+'.a' in concepts:
            concept2 += '.a'
        elif concept2+'.adv' in concepts:
            concept2 += '.adv'
        else:
            continue

        g.append(tuple([concept1, concept2, chance[2]]))