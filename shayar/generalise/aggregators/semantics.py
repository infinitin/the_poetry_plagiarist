__author__ = 'Nitin'
from itertools import combinations
from pattern.text.en import tag, wordnet, lemma
from collections import Counter
import logging



def agg_character_hypernyms(poems, template):
    all_characters = []
    for poem in poems:
        all_characters.extend(poem.characters)

    #Get the synsets of the operative word in each of the characters
    all_synsets = [synset(character.text) for character in all_characters]
    all_synsets = [s for s in all_synsets if s is not None]

    all_common_ancestors = []
    for pair in combinations(all_synsets, 2):
        all_common_ancestors.append(str(wordnet.ancestor(*pair)).partition("'")[-1].rpartition("'")[0])

    template.hypernym_ancestors = all_common_ancestors


def synset(phrase):
    for word, pos in tag(phrase):
        if pos.startswith('N'):
            try:
                return wordnet.synsets(lemma(word))[0]
            except IndexError:
                logging.error('Could not find synset for: ' + phrase)
                return None
        elif pos == 'PRP':
            return wordnet.synsets('living thing')[0]

