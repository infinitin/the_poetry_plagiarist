__author__ = 'Nitin'

import nltk
import string
from nltk.corpus import cmudict


def count_syllables(poem):
    syllabic_line_lengths = []
    for line in poem:
        exclude = set(string.punctuation)
        no_punct_line = ''.join(char for char in line if char not in exclude)
        tokenized_line = nltk.Text(nltk.word_tokenize(no_punct_line))
        words = [w.lower() for w in tokenized_line]
        syllabic_line_length = 0
        for word in words:
            syllabic_line_length += __count_syllables_in_word(word)
        syllabic_line_lengths.append(syllabic_line_length)

    return syllabic_line_lengths


def __count_syllables_in_word(word):
    dictionary = cmudict.dict()
    syllables = 0
    try:
        arpabet_word = dictionary[word][0]
        for phoneme in arpabet_word:
            if str(phoneme[-1]).isdigit():
                syllables += 1
    except KeyError:
        if word.endswith("n't") and not (word.equals("can't") or word.startswith("won't") or word.startswith("ain't")):
            syllables += 2
        else:
            syllables += 1

    return syllables