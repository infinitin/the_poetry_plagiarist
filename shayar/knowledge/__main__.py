__author__ = 'Nitin'
from collocations import get_knowledge_from_collocations
from associations import get_knowledge_from_associations
from pattern.db import Datasheet
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)

knowledge = get_knowledge_from_collocations() + get_knowledge_from_associations()

ds = Datasheet()
for speck in knowledge:
    ds.append(speck)

ds.save('knowledge.csv')