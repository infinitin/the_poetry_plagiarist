__author__ = 'Nitin'
from pattern.text.en import wordnet, singularize
from pattern.text.en import lemma as lemmatise
import logging


def get_knowledge_from_wordnet(g):
    logging.info('Gathering knowledge from wordnet')
    concepts = set([head for head, tail, relation in g] + [tail for head, tail, relation in g])
    for concept in concepts:
        word, pos = concept.split('.')
        if pos != 'n':
            continue

        synset = get_synset(word. wordnet.NOUN)
        if synset is None:
            continue

        hypernyms = ([str(hypernym).partition("'")[-1].rpartition("'")[0] for hypernym in synset.hypernyms()])
        for hypernym in hypernyms:
            g.append(tuple([word, hypernym, 'IsA']))


def get_synset(word, wpos):
    synset = None
    try:
        synset = wordnet.synsets(singularize(lemmatise(word)), wpos)[0]
    except IndexError:
        try:
            synset = wordnet.synsets(lemmatise(word), wpos)[0]
        except IndexError:
            try:
                synset = wordnet.synsets(singularize(word), wpos)[0]
            except IndexError:
                try:
                    synset = wordnet.synsets(word, wpos)[0]
                except IndexError:
                    pass

    return synset