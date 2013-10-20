__author__ = 'Nitin'

import nltk
import string
from nltk.corpus import cmudict


def __get_phonemes(line, vowel):
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

        if vowel:
            for phoneme in arpabet_word:
                if str(phoneme[-1]).isdigit():
                    phonemes.append(phoneme)
        else:
            for phoneme in arpabet_word:
                if not str(phoneme[-1]).isdigit():
                    phonemes.append(phoneme)

    return phonemes


def detect_assonance(poem):
    assonance_lengths = []

    for line in poem:
        vowel_phonemes = __get_phonemes(line, True)
        assonance_lengths.append(len(vowel_phonemes) - len(set(vowel_phonemes)))

    return assonance_lengths


def detect_consonance(poem):
    consonance_lengths = []

    for line in poem:
        consonant_phonemes = __get_phonemes(line, False)
        consonance_lengths.append(len(consonant_phonemes) - len(set(consonant_phonemes)))

    return consonance_lengths


def detect_alliteration(poem):
    alliteration_lengths = []

    for line in poem:
        alliteration_phonemes = __get_start_or_stressed_phonemes(line)
        alliteration_lengths.append(len(alliteration_phonemes) - len(set(alliteration_phonemes)))

    return alliteration_lengths


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
        for phoneme in word:
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





