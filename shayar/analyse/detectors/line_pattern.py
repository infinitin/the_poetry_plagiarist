from __future__ import division
__author__ = 'Nitin'


import utils
from utils import get_tokenized_words


def detect_assonance(poem):
    return __detect_pattern(poem, False, False)


def detect_consonance(poem):
    return __detect_pattern(poem, True, False)


def detect_alliteration(poem):
    return __detect_pattern(poem, False, True)


# Grab the phonemes that we care about
# Find the number of repeated chosen phonemes
# Normalise it (more investigation needed perhaps)
def __detect_pattern(poem, consonance, alliteration):
    pattern_lengths = []

    for line in poem:
        phonemes = __get_start_or_stressed_phonemes(line) if alliteration else __get_phonemes(line, consonance)
        normalizer = len(set(phonemes)) if consonance else len(line.split(' '))
        normalized_count = (len(phonemes) - len(set(phonemes)) + 1)/normalizer
        pattern_lengths.append(normalized_count)

    return pattern_lengths


# Get the phonemes in the line
# If is_consonant is true then we only grab the consonant phonemes, otherwise we grab the vowels phonemes
def __get_phonemes(line, is_consonant):
    words = get_tokenized_words(line)

    phonemes = []
    for word in words:
        try:
            arpabet_word = utils.dictionary[word][0]
        except KeyError:
            continue

        if is_consonant:
            phonemes.extend([phoneme for phoneme in arpabet_word if not str(phoneme[-1]).isdigit()])
        else:
            phonemes.extend([phoneme for phoneme in arpabet_word if str(phoneme[-1]).isdigit()])

    return phonemes


# Alliteration occurs when consonants are repeated at the beginning or on the stressed syllable of consecutive words.
# So this grabs the stressed consonant or otherwise the first consonant of each word in the line.
def __get_start_or_stressed_phonemes(line):
    words = get_tokenized_words(line)

    phonemes = []
    for word in words:
        try:
            arpabet_word = utils.dictionary[word][0]
        except KeyError:
            continue

        previous_phoneme = ""
        first_found = False
        for phoneme in arpabet_word:
            if not str(phoneme[-1]).isdigit():
                if not first_found:
                    phonemes.append(phoneme)
                    first_found = True
                else:
                    previous_phoneme = phoneme
            else:
                if str(phoneme[-1]) == utils.stressed:
                    phonemes.append(previous_phoneme)

    return phonemes





