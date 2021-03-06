__author__ = 'Nitin'
from BeautifulSoup import BeautifulSoup
import os
import logging

COLLOCS_DATA_LOC = 'C:\\Python27\\collocations_data\\files\\'


def get_knowledge_from_collocations(g):
    build_knowledge_graph_from_collocations(g)
    build_verbs_knowledge_graph_from_collocations(g)


def build_knowledge_graph_from_collocations(g):
    logging.info('Gathering knowledge from collocations')
    #For each file in the dictionary
    for subdir, dirs, files in os.walk(COLLOCS_DATA_LOC):
        nouns = [file_name for file_name in files if 'noun.htm' in file_name]
        for noun in nouns:
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
                elif 'NOUN' in u:
                    relation = 'RelatedTo'

                if not relation:
                    continue

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
                        new_word.replace('sb', '')
                        new_word.replace('sth', '')

                        reject = ['.', '~', "'"]
                        rejection = [r for r in reject if r in new_word]
                        if rejection:
                            continue

                        if '/' in new_word:
                            tokens = new_word.split()
                            before = ''
                            after = ''
                            slash_token = ''
                            for token in tokens:
                                if '/' in token:
                                    slash_token = token
                                    before = token[:token.index('/')]
                                    after = token[token.index('/') + 1:]
                                    break

                            words.append(new_word.replace(slash_token, before))
                            words.append(new_word.replace(slash_token, after))
                        else:
                            new_word.replace('  ', ' ')
                            words.append(new_word)

                    for word in words:
                        if relation == 'ReceivesAction' or relation == 'TakesAction':
                            g.append(tuple([noun.partition('_')[0] + '.n', word + '.v', relation]))
                        elif relation == 'HasProperty':
                            g.append(tuple([noun.partition('_')[0] + '.n', word + '.a', relation]))
                        elif relation == 'RelatedTo':
                            g.append(tuple([noun.partition('_')[0] + '.n', word + '.n', relation]))


def build_verbs_knowledge_graph_from_collocations(g):
    #For each file in the dictionary
    for subdir, dirs, files in os.walk(COLLOCS_DATA_LOC):
        verbs = [file_name for file_name in files if 'verb.htm' in file_name]
        for verb in verbs:
            root = BeautifulSoup(open(COLLOCS_DATA_LOC + verb))
            ps = root('p')
            for p in ps:
                u = p.findAll('u')
                if not u:
                    continue
                u = u[0].text
                if 'ADV' in u:
                    relation = 'HasProperty'
                else:
                    continue

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
                        new_word.replace('sb', '')
                        new_word.replace('sth', '')

                        reject = ['.', '~', "'"]
                        rejection = [r for r in reject if r in new_word]
                        if rejection:
                            continue

                        if '/' in new_word:
                            tokens = new_word.split()
                            before = ''
                            after = ''
                            slash_token = ''
                            for token in tokens:
                                if '/' in token:
                                    slash_token = token
                                    before = token[:token.index('/')]
                                    after = token[token.index('/') + 1:]
                                    break

                            words.append(new_word.replace(slash_token, before))
                            words.append(new_word.replace(slash_token, after))
                        else:
                            new_word.replace('  ', ' ')
                            words.append(new_word)

                    for word in words:
                        g.append(tuple([verb.partition('_')[0] + '.v', word + '.adv', relation]))