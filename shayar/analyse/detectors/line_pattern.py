from __future__ import division
__author__ = 'Nitin'


import nltk
import string
from nltk.corpus import cmudict


def detect_assonance(poem):
    return __detect_pattern(poem, False, False)


def detect_consonance(poem):
    return __detect_pattern(poem, True, False)


def detect_alliteration(poem):
    return __detect_pattern(poem, False, True)


def __detect_pattern(poem, consonance, alliteration):
    pattern_lengths = []

    for line in poem:
        phonemes = __get_start_or_stressed_phonemes(line) if alliteration else __get_phonemes(line, consonance)
        normalizer = len(set(phonemes)) if consonance else len(line.split(' '))
        normalized_count = (len(phonemes) - len(set(phonemes)) + 1)/normalizer
        pattern_lengths.append(normalized_count)

    return pattern_lengths


def __get_phonemes(line, is_consonant):
    dictionary = cmudict.dict()
    exclude = set(string.punctuation)
    no_punct_line = ''.join(char for char in line if char not in exclude)
    tokenized_line = nltk.Text(nltk.word_tokenize(no_punct_line))
    words = [w.lower() for w in tokenized_line]

    phonemes = []
    for word in words:
        try:
            arpabet_word = dictionary[word][0]
        except KeyError:
            continue

        if is_consonant:
            for phoneme in arpabet_word:
                if not str(phoneme[-1]).isdigit():
                    phonemes.append(phoneme)
        else:
            for phoneme in arpabet_word:
                if str(phoneme[-1]).isdigit():
                    phonemes.append(phoneme)

    return phonemes


def __get_start_or_stressed_phonemes(line):
    dictionary = cmudict.dict()
    exclude = set(string.punctuation)
    no_punct_line = ''.join(char for char in line if char not in exclude)
    tokenized_line = nltk.Text(nltk.word_tokenize(no_punct_line))
    words = [w.lower() for w in tokenized_line]

    phonemes = []
    for word in words:
        try:
            arpabet_word = dictionary[word][0]
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
                if str(phoneme[-1]) == "1":
                    phonemes.append(previous_phoneme)

    return phonemes





