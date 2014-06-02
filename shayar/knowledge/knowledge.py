__author__ = 'Nitin'
from pattern.db import CSV
from pattern.graph import Graph
from pattern.text.en import wordnet, singularize
from pattern.text.en import lemma as lemmatise
from wordnik import swagger, WordApi
from urllib2 import HTTPError
import random
import logging
from urllib2 import urlopen, URLError
from json import loads as json_load
from shayar.generate.framenet_reader import get_random_word
import sys

apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'd2194ae1a0c4be586853d0828d10f77db48039209ef684218'
client = swagger.ApiClient(apiKey, apiUrl)
wordApi = WordApi.WordApi(client)

graph = Graph()

w = {
    'V': wordnet.VERB,
    'VB': wordnet.VERB,
    'N': wordnet.NOUN,
    'NN': wordnet.NOUN,
    'A': wordnet.ADJECTIVE,
    'ADV': wordnet.ADVERB,
    'AVP': wordnet.ADVERB
}


def closest_matching(candidate_nodes, context_nodes):
    candidate_nodes = remove_none(candidate_nodes)
    context_nodes = remove_none(context_nodes)
    if len(candidate_nodes) <= 1 or not context_nodes:
        return set(candidate_nodes)

    h = lambda id1, id2: 1 - int('RelatedTo' in graph.edge(id1, id2).type)
    shortest_path_length = sys.maxint
    closest_candidate_nodes = set()
    for context_node in context_nodes:
        for candidate_node in candidate_nodes:
            logging.info('Similarity between ' + candidate_node.id + ' ' + context_node.id)
            spl = graph.shortest_path(candidate_node, context_node, heuristic=h)
            if spl is None:
                continue
            if len(spl) < shortest_path_length:
                closest_candidate_nodes = {candidate_node}
                shortest_path_length = len(spl) - 1
                if shortest_path_length == 1:
                    return closest_candidate_nodes
            elif len(spl) == shortest_path_length:
                closest_candidate_nodes.add(candidate_node)

    if not closest_candidate_nodes:
        return set(candidate_nodes)

    return closest_candidate_nodes


def new_concepts(context_nodes):
    new_concept_nodes = set()
    for context_node in context_nodes:
        new_concept_nodes.add(halo(context_node))
        new_concept_nodes.add(field(context_node))

    return new_concept_nodes


def get_all_nodes(l):
    return remove_none([get_node(word, pos) for word, pos in l])


#Given a noun, give me an action that it receives
def get_receives_action(noun):
    nouns = []
    target_node = get_node(noun, 'n')
    if target_node is not None:
        nouns = [n.id.split('.')[0] for n in halo(target_node, relation='ReceivesAction')]
        if nouns:
            return random.choice(nouns)

    logging.info(noun + '.n is not in the graph')
    synonyms = get_synonyms(noun, wordnet.NOUN)
    synonym_nodes = remove_none([get_node(synonym, 'n') for synonym in synonyms])
    if not synonym_nodes:
        logging.info('No nodes: ' + str(synonyms))
        return get_random_word('V')

    for synonym_node in synonym_nodes:
        nouns.extend([n.id.split('.')[0] for n in halo(synonym_node, relation='ReceivesAction')])

    if nouns:
        return random.choice(nouns)
    else:
        return get_random_word('V')


def get_action_taker_receiver(action, action_relation):
    nouns = []
    target_node = get_node(action, 'v')
    if target_node is not None:
        nouns = [n.id.split('.')[0] for n in field(target_node, relation=action_relation)]
        if nouns:
            return random.choice(nouns)

    logging.info(action + '.v is not in the graph')
    synonyms = get_synonyms(action, wordnet.VERB)
    synonym_nodes = remove_none([get_node(synonym, 'v') for synonym in synonyms])
    if not synonym_nodes:
        logging.info('No nodes: ' + str(synonyms))
        return get_random_word('N')

    for synonym_node in synonym_nodes:
        nouns.extend([n.id.split('.')[0] for n in field(synonym_node, relation=action_relation)])

    if nouns:
        return random.choice(nouns)
    else:
        return get_random_word('N')


def get_property(target_word, pos, used):
    properties = []
    target_node = get_node(target_word, pos.lower())
    if target_node is not None:
        properties = [n.id.split('.')[0] for n in halo(target_node, relation='HasProperty')]
        return random.choice([prop for prop in properties if prop not in used])

    else:
        logging.info(target_word + '.' + pos.lower() + ' is not in the graph')
        synonyms = get_synonyms(target_word, w[pos])
        synonym_nodes = remove_none([get_node(synonym, pos.lower()) for synonym in synonyms])
        if not synonym_nodes:
            logging.info('No nodes: ' + str(synonyms))
            if pos.startswith('V'):
                return get_random_word('AVP')
            else:
                return get_random_word('A')

        for synonym_node in synonym_nodes:
            properties.extend([n.id.split('.')[0] for n in halo(synonym_node, relation='HasProperty')])

        if properties:
            return random.choice([prop for prop in properties if prop not in used])
        else:
            if pos.startswith('V'):
                return get_random_word('AVP')
            else:
                return get_random_word('A')


def get_synonyms(word, pos=None, extended=False):
    if extended:
        logging.info('Getting extended synonyms for ' + word)
    else:
        logging.info('Getting synonyms for ' + word)
    synonyms = []

    if pos is not None:
        synset = get_synset(word, pos=pos)
    else:
        synset = get_synset(word)

    if synset:
        synonyms.extend(synset.synonyms)
        synonyms.extend([str(holonym).partition("'")[-1].rpartition("'")[0] for holonym in synset.holonyms()])
        synonyms.extend([str(hypernym).partition("'")[-1].rpartition("'")[0] for hypernym in synset.hypernyms()])

    if extended:
        try:
            wordnik_synonyms = wordApi.getRelatedWords(word, relationshipTypes='synonym')[0].words
            synonyms.extend(wordnik_synonyms)
        except (TypeError, HTTPError):
            pass

    return synonyms


def get_synset(word, pos=''):
    synset = None
    try:
        if pos:
            synset = wordnet.synsets(singularize(lemmatise(word)), w[pos])[0]
        else:
            synset = wordnet.synsets(singularize(lemmatise(word)))[0]
    except IndexError:
        try:
            if pos:
                synset = wordnet.synsets(lemmatise(word), w[pos])[0]
            else:
                synset = wordnet.synsets(lemmatise(word))[0]
        except IndexError:
            try:
                if pos:
                    synset = wordnet.synsets(singularize(word), w[pos])[0]
                else:
                    synset = wordnet.synsets(singularize(word))[0]
            except IndexError:
                try:
                    if pos:
                        synset = wordnet.synsets(word, w[pos])[0]
                    else:
                        synset = wordnet.synsets(word)[0]
                except IndexError:
                    pass

    if pos and synset is None:
        return get_synset(word)

    return synset


def get_hypernyms(isa):
    hypernyms = []
    ps = ['n', 'v', 'a', 'adv']
    for p in ps:
        target_node = get_node(isa, p)
        if target_node is not None:
            hypernyms.extend([n.id.split('.')[0] for n in halo(target_node, relation='HasProperty')])

    isa_synset = get_synset(isa.split()[0])
    if isa_synset:
        hypernyms.extend([str(hypernym).partition("'")[-1].rpartition("'")[0] for hypernym in isa_synset.hypernyms()])

    return hypernyms


def get_node(word, pos):
    try:
        return graph.node(lemmatise(word) + '.' + pos.lower())
    except KeyError:
        return None


def remove_none(xs):
    return [x for x in xs if x is not None]


def field(node, relation='', depth=1, fringe=0):
    def traversable(node, edge):
        return edge.node2 == node and edge.type == relation

    if relation:
        g = node.graph.copy(nodes=node.flatten(depth, traversable))
    else:
        g = node.graph.copy(nodes=node.flatten(depth))
    g = g.fringe(depth=fringe)
    g = [node.graph[n.id] for n in g if n != node]
    return g


def halo(node, relation='', depth=1, fringe=0):
    if not relation:
        return node.flatten(depth)

    def traversable(node, edge):
        return edge.node1 == node and edge.type == relation

    if relation:
        g = node.graph.copy(nodes=node.flatten(depth, traversable))
    else:
        g = node.graph.copy(nodes=node.flatten(depth))
    g = g.fringe(depth=fringe)
    g = [node.graph[n.id] for n in g if n != node]
    return g


def retrieve_knowledge():
    logging.info('Retrieving knowledge')
    data = 'C:\\Users\\Lenovo\\PycharmProjects\\the_poetry_plagiarist\\shayar\\knowledge\\knowledge.csv'
    data = CSV.load(data)
    for concept1, concept2, relation in data:
        graph.add_edge(concept1, concept2, type=relation)
        if 'Related' in relation:
            graph.add_edge(concept2, concept1, type=relation)


#Find the most conceptually similar words from a list of candidates
def most_similar(word, candidates, pos):
    best_similarity_score = sys.maxint
    best_similarity_candidate = ''
    word_synset = get_synset(word, pos)

    if word_synset is None:
        wpos = wordnet.NOUN
        if pos.startswith('AVP'):
            wpos = wordnet.ADVERB
        elif pos.startswith('A'):
            wpos = wordnet.ADJECTIVE
        elif pos.startswith('V'):
            wpos = wordnet.VERB
        synonyms = get_synonyms(word, wpos, True)
        for candidate in candidates:
            if candidate in synonyms:
                return candidate, 2

        return random.choice(candidates), best_similarity_score

    for candidate in candidates:
        candidate_synset = get_synset(candidate, pos)
        if candidate_synset is None:
            continue
        try:
            similarity = wordnet.similarity(word_synset, candidate_synset)
        except AttributeError:
            continue
        if similarity < best_similarity_score:
            best_similarity_score = similarity
            best_similarity_candidate = candidate

    if best_similarity_candidate:
        return best_similarity_candidate, best_similarity_score
    else:
        return random.choice(candidates), best_similarity_score


def get_action_theme(valence_pattern, action, obj):
    logging.info('Getting action theme for ' + action + ' ' + obj)
    prep = ''
    for group in valence_pattern:
        for valence_unit in group:
            pos = valence_unit.get('PT')
            if pos.startswith('P'):
                prep = pos.partition('[')[-1].rpartition(']')[0]

    if not prep:
        return ''

    #Make an API request to Google autocomplete
    url = "http://suggestqueries.google.com/complete/search?client=firefox&q="
    if obj:
        request_url = url + ' '.join([action, obj, prep]) + ' '
    else:
        request_url = url + ' '.join([action, prep]) + ' '
    request_url = request_url.replace(' ', '%20')

    try:
        socket = urlopen(request_url)
        json = json_load(socket.read())
        socket.close()
    except URLError:
        raise Exception("You are not connected to the Internet!")

    suggestions = json[1]
    original = json[0]
    for suggestion in suggestions:
        if 'www' in suggestion:
            continue
        stripped = suggestion.replace(original, '')
        words = stripped.split()
        if len(words) > 1:
            continue
        return stripped

    return get_random_word('N')