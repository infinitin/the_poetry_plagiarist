__author__ = 'Nitin'
from pattern.text.en import wordnet, singularize
from pattern.text.en import lemma as lemmatise
import logging


def get_knowledge_from_wordnet(g):
    logging.info('Gathering knowledge from wordnet')
    concepts = set([head for head, tail, relation in g if head.endswith('.n')] + [tail for head, tail, relation in g if
                                                                                  tail.endswith('.n')])
    for concept in concepts:
        word, pos = concept.split('.')
        if pos != 'n':
            continue

        try:
            synset = get_synset(word.split()[-1], wordnet.NOUN)
        except IndexError:
            continue
        if synset is None:
            continue

        hypernyms = ([str(hypernym).partition("'")[-1].rpartition("'")[0] for hypernym in synset.hypernyms()])
        for hypernym in hypernyms:
            g.append(tuple([concept, hypernym + '.n', 'IsA']))

        meronyms = ([str(meronym).partition("'")[-1].rpartition("'")[0] for meronym in synset.meronyms()])
        for meronym in meronyms:
            g.append(tuple([concept, meronym + '.n', 'PartOf']))

        holonyms = ([str(holonym).partition("'")[-1].rpartition("'")[0] for holonym in synset.holonyms()])
        for holonym in holonyms:
            if holonym + '.n' not in concepts:
                g.append(tuple([holonym + '.n', concept, 'IsA']))


def get_synset(word, wpos):
    synset = None
    try:
        synset = wordnet.synsets(singularize(lemmatise(word)), wpos)[0]
    except IndexError:
        pass

    return synset