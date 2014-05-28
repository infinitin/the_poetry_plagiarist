__author__ = 'Nitin'
from collocations import build_knowledge_graph_from_collocations
import cPickle
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)

collocations_knowldege = build_knowledge_graph_from_collocations()

#Pickle it.
out = open('collocations.knowledge', 'wb+')
out.truncate()
cPickle.dump(collocations_knowldege, out, -1)
out.close()