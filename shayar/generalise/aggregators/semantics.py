__author__ = 'Nitin'
from itertools import combinations, izip_longest
from pattern.text.en import tag, wordnet, singularize
from pattern.text.en import lemma as lemmatise
from collections import Counter
import logging


def agg_hypernym_ancestors(poems, template):
    logging.info('Starting aggregator: agg_character_hypernyms')
    all_characters = []
    for poem in poems:
        all_characters.extend(poem.characters)

    #Get the synsets of the operative word in each of the characters
    all_synsets = [get_synset(character.text) for character in all_characters]
    all_synsets = [s for s in all_synsets if s is not None]

    all_hypernyms = []
    for synset in all_synsets:
        all_hypernyms.extend(
            [str(hypernym).partition("'")[-1].rpartition("'")[0] for hypernym in synset.hypernyms(recursive=True)])

    #Now filter by the ones that actually occur with some significant frequency
    min_num_occurrences = round(len(all_synsets) * 0.05)
    counts = Counter(all_hypernyms)
    template.hypernym_ancestors.extend(
        [(hypernym, count) for hypernym, count in counts.items() if
         count > min_num_occurrences and hypernym != 'entity'])

    logging.info('Aggregator finished: agg_character_hypernyms')


def get_synset(phrase):
    synset = None
    for word, pos in tag(phrase):
        if pos.startswith('N') and word != 'of':
            try:
                synset = wordnet.synsets(singularize(lemmatise(word)))[0]
            except IndexError:
                try:
                    synset = wordnet.synsets(lemmatise(word))[0]
                except IndexError:
                    try:
                        synset = wordnet.synsets(singularize(word))[0]
                    except IndexError:
                        try:
                            synset = wordnet.synsets(word)[0]
                        except IndexError:
                            logging.error("Failed to find synset for '" + word + "'")
                            continue
        elif pos == 'PRP':
            return wordnet.synsets('living thing')[0]

    return synset


def agg_polarity_by_line(poems, template):
    logging.info('Starting aggregator: agg_polarity_by_line')
    all_polarity = [poem.polarity_by_line for poem in poems]
    template.polarity_by_line = list(izip_longest(*all_polarity))
    logging.info('Aggregator finished: agg_polarity_by_line')


def agg_subjectivity_by_line(poems, template):
    logging.info('Starting aggregator: agg_subjectivity_by_line')
    all_subjectivity = [poem.subjectivity_by_line for poem in poems]
    template.subjectivity_by_line = list(izip_longest(*all_subjectivity))
    logging.info('Aggregator finished: agg_subjectivity_by_line')


def agg_modality_by_line(poems, template):
    logging.info('Starting aggregator: agg_modality_by_line')
    all_modality = [poem.modality_by_line for poem in poems]
    template.modality_by_line = list(izip_longest(*all_modality))
    logging.info('Aggregator finished: agg_modality_by_line')


def agg_mood_by_line(poems, template):
    logging.info('Starting aggregator: agg_mood_by_line')
    all_mood = [poem.mood_by_line for poem in poems]
    template.mood_by_line = list(izip_longest(*all_mood))
    logging.info('Aggregator finished: agg_mood_by_line')
