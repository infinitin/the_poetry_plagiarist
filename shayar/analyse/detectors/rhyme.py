__author__ = 'Nitin'

from utils import get_stanzas
import utils
from utils import get_tokenized_words
from utils import get_pronunciations
from itertools import product


def determine_rhyme_scheme(poem):
    stanzas = get_stanzas(poem)
    stanza_rhyme_scheme = []

    for stanza in stanzas:
        last_words = []

        for line in stanza:
            if line.strip():
                last_word = get_tokenized_words(line)[-1]
                last_words.append(get_pronunciations(last_word))

        stanza_rhyme_scheme.append(__get_rhyme_scheme(last_words))

    return stanza_rhyme_scheme


def detect_internal_rhyme(poem):
    stanzas = get_stanzas(poem)
    rhyme_scheme = []

    for stanza in stanzas:
        words = []

        for line in stanza:
            line_words = get_tokenized_words(line)

            for word in line_words:
                words.append(get_pronunciations(word))

        rhyme_scheme.append(__get_rhyme_scheme(words))

    return rhyme_scheme


# Create a map of a rhyme token to the rhyme phoneme
# When determining the rhyme token to assign, check if it has been to the map first, or otherwise add it
# Some words have more than one pronunciation so we need to take both into account and give all permutations in the
#  generalisation stage
# If there is only one permutation, we show it as a single list. May want to remove this.
def __get_rhyme_scheme(words):
    rhyme_scheme_map = {}
    rhyme_scheme = []
    line_rhyme_token = 'A'

    for pronunciations in words:
        rhyme_tokens = []

        for pronunciation in pronunciations:
            index = 0

            for phoneme in pronunciation:
                if str(phoneme[-1]).isdigit() and str(phoneme[-1]) == utils.stressed:
                    rhyme_phonemes = __get_rhyme_phonemes(pronunciation[index:])

                    if not rhyme_phonemes in rhyme_scheme_map:
                        rhyme_scheme_map[rhyme_phonemes] = line_rhyme_token
                        line_rhyme_token = chr(ord(line_rhyme_token)+1)
                    else:
                        if phoneme == '':
                            rhyme_tokens.append(line_rhyme_token)
                            line_rhyme_token = chr(ord(line_rhyme_token)+1)

                    rhyme_tokens.append(rhyme_scheme_map[rhyme_phonemes])
                index += 1

        rhyme_tokens = list(set(rhyme_tokens))
        rhyme_scheme.append(rhyme_tokens)

    return list(product(*rhyme_scheme))


# The phonemes that determine rhyme are the vowels and the last consonant.
# E.g. Tragedy and strategy rhyme (well... near rhyme, but we want to spot that.)
# Can have separate rules for strict and near rhyme, but we prefer to assume rhyme in the generalisation stage
def __get_rhyme_phonemes(phonemes):
    rhyme_phonemes = []

    for phoneme in phonemes:
        if str(phoneme[-1]).isdigit() or phonemes[-1] == phoneme:
            rhyme_phonemes.append(phoneme)

    return str(rhyme_phonemes)
