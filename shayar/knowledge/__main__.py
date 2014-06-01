__author__ = 'Nitin'
from collocations import get_knowledge_from_collocations
from associations import get_knowledge_from_associations
from common_sense import get_knowledge_from_pattern_common_sense
from wordnet_nyms import get_knowledge_from_wordnet
from pattern.db import Datasheet
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)

g = []
get_knowledge_from_collocations(g)
get_knowledge_from_associations(g)
get_knowledge_from_pattern_common_sense(g)

g = [tuple([head.strip(), tail.strip(), relation]) for head, tail, relation in g if '.' in head and '.' in tail]
#get_knowledge_from_wordnet(g)

knowledge = []
for speck in g:
    if speck not in knowledge:
        knowledge.append(speck)

logging.info('Memorising...')
ds = Datasheet()
for speck in knowledge:
    ds.append(speck)

ds.save('knowledge.csv')