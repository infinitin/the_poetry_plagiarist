__author__ = 'Nitin'
from pattern.db import CSV
import logging


def get_knowledge_from_pattern_common_sense():
    logging.info('Gathering knowledge from pattern common sense relations')
    g = []
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
            g.append(tuple([concept1, concept2, 'NotRelatedTo']))
        elif relation == 'is-related-to':
            g.append(tuple([concept1, concept2, 'RelatedTo']))
        elif relation == 'is-same-as':
            g.append(tuple([concept1, concept2, 'RelatedTo']))
        elif relation == 'is-effect-of':
            g.append(tuple([concept1, context, 'RelatedTo']))

        if context == 'people':
            g.append(tuple([concept1, 'person', 'IsA']))

    return g
