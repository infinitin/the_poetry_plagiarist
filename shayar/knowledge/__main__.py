__author__ = 'Nitin'
from collocations import get_knowledge_from_collocations
from associations import get_knowledge_from_associations
from common_sense import get_knowledge_from_pattern_common_sense
from pattern.db import Datasheet
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)

knowledge = get_knowledge_from_collocations() + \
            get_knowledge_from_associations() + \
            get_knowledge_from_pattern_common_sense()

#clean(knowledge)

logging.info('Memorising...')
ds = Datasheet()
for speck in knowledge:
    ds.append(speck)

ds.save('knowledge.csv')