__author__ = 'Nitin'
from BeautifulSoup import BeautifulSoup
import os
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
                        contents = b.contents[0]
                    except IndexError:
                        continue
                    contents = contents.replace('|', ',').split(',')
                    words = []
                    for word in contents:
                        new_word = word.strip()
                        new_word.replace('(', '')
                        new_word.replace(')', '')
                        if not new_word or '.' in new_word:
                            continue
                        new_word = new_word.replace('sb','')
                        new_word = new_word.replace('sth','')
                        new_word = new_word.replace('~s','')
                        new_word = new_word.replace('~','')
                        if '/' in new_word:
                            tokens = new_word.split()
                            before = ''
                            after = ''
                            slash_token = ''
                            for token in tokens:
                                if '/' in token:
                                    slash_token = token
                                    before = token[:token.index('/')]
                                    after = token[token.index('/')+1:]
                                    break

                            words.append(new_word.replace(slash_token, before))
                            words.append(new_word.replace(slash_token, after))
                        else:
                            words.append(new_word)

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
                        contents = b.contents[0]
                    except IndexError:
                        continue
                    contents = contents.replace('|', ',').split(',')
                    words = []
                    for word in contents:
                        new_word = word.strip()
                        new_word.replace('(', '')
                        new_word.replace(')', '')
                        if not new_word or '.' in new_word:
                            continue
                        new_word = new_word.replace('sb','')
                        new_word = new_word.replace('sth','')
                        new_word = new_word.replace('~s','')
                        new_word = new_word.replace('~','')
                        if '/' in new_word:
                            tokens = new_word.split()
                            before = ''
                            after = ''
                            slash_token = ''
                            for token in tokens:
                                if '/' in token:
                                    slash_token = token
                                    before = token[:token.index('/')]
                                    after = token[token.index('/')+1:]
                                    break

                            words.append(new_word.replace(slash_token, before))
                            words.append(new_word.replace(slash_token, after))
                        else:
                            words.append(new_word)

                    for word in words:
                        g.append(tuple([noun.partition('_')[0], word, relation]))

    return g