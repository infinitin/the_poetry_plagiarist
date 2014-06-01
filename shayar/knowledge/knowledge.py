__author__ = 'Nitin'
from pattern.db import CSV
from pattern.graph import Graph
import logging

graph = Graph()


def retrieve_knowledge():
    logging.info('Retrieving knowledge')
    data = 'knowledge.csv'
    data = CSV.load(data)
    for concept1, concept2, relation in data:
        graph.add_edge(concept1, concept2, type=relation)
        if 'Related' in relation:
            graph.add_edge(concept2, concept1, type=relation)