__author__ = 'Nitin'
from BeautifulSoup import BeautifulSoup
import os
from shayar.analyse.detectors.utils import get_tokenized_words
import logging

COLLOCS_DATA_LOC = 'C:\\Python27\\collocations_data\\files\\'


def build_knowledge_graph_from_collocations():
    g = []
    logging.info('Parsing')
    #For each file in the dictionary
    for subdir, dirs, files in os.walk(COLLOCS_DATA_LOC):
        nouns = [file_name for file_name in files if 'noun.htm' in file_name]
        for noun in nouns:
            logging.info('Parsing ' + str(noun))
            root = BeautifulSoup(open(COLLOCS_DATA_LOC + noun))
            ps = root('p')
            for p in ps:
                u = p.findAll('u')
                if not u:
                    continue
                u = u[0].text
                relation = ''
                if 'VERB +' in u:
                    relation = 'ReceivesAction'
                elif '+ VERB' in u:
                    relation = 'TakesAction'
                elif 'ADJ' in u:
                    relation = 'HasProperty'

                bs = p.findAll('b')
                for b in bs:
                    try:
                        words = [word for word in get_tokenized_words(b.contents) if word != ',' and word != '|']
                    except TypeError:
                        continue
                    for word in words:
                        g.append(tuple([noun.partition('_')[0], word, relation]))

    return g


def build_verbs_knowledge_graph_from_collocations():
    g = []
    logging.info('Parsing')
    #For each file in the dictionary
    for subdir, dirs, files in os.walk(COLLOCS_DATA_LOC):
        nouns = [file_name for file_name in files if 'verb.htm' in file_name]
        for noun in nouns:
            logging.info('Parsing ' + str(noun))
            root = BeautifulSoup(open(COLLOCS_DATA_LOC + noun))
            ps = root('p')
            for p in ps:
                u = p.findAll('u')
                if not u:
                    continue
                u = u[0].text
                relation = ''
                if 'ADV' in u:
                    relation = 'HasProperty'

                bs = p.findAll('b')
                for b in bs:
                    try:
                        words = [word for word in get_tokenized_words(b.contents) if word != ',' and word != '|']
                    except TypeError:
                        continue
                    for word in words:
                        g.append(tuple([noun.partition('_')[0], word, relation]))

    return g