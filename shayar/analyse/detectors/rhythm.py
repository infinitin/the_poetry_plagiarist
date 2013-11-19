__author__ = 'Nitin'

import nltk
import string
from utils import get_stanzas
import utils


def count_syllables(poem):
    stanzas = get_stanzas(poem)
    syllabic_stanza_lengths = []

    for stanza in stanzas:
        syllabic_line_lengths = []

        for line in stanza:
            exclude = set(string.punctuation)
            exclude.remove("'")
            exclude.remove("-")

            no_punct_line = ''.join(char for char in line if char not in exclude)
            no_punct_line = no_punct_line.replace(" '", " ")
            no_punct_line = no_punct_line.replace("-", " ")

            tokenized_line = nltk.Text(nltk.word_tokenize(no_punct_line))
            words = [w.lower() for w in tokenized_line]

            syllabic_line_length = 0
            for word in words:
                syllabic_line_length += __count_syllables_in_word(word, utils.dictionary)

            syllabic_line_lengths.append(syllabic_line_length)

        syllabic_stanza_lengths.append(syllabic_line_lengths)

    return syllabic_stanza_lengths


def get_stress_pattern(poem):
    stress_patterns = []

    for line in poem:
        exclude = set(string.punctuation)
        exclude.remove("'")
        exclude.remove("-")

        no_punct_line = ''.join(char for char in line if char not in exclude)
        no_punct_line = no_punct_line.replace(" '", " ")
        no_punct_line = no_punct_line.replace("-", " ")

        tokenized_line = nltk.Text(nltk.word_tokenize(no_punct_line))
        words = [w.lower() for w in tokenized_line]

        stress_pattern = ""
        for word in words:
            try:
                phonemes = utils.dictionary[word][0]
                for phoneme in phonemes:
                    if str(phoneme[-1]).isdigit():
                        stress_pattern += str(phoneme[-1])
            except KeyError:
                if word.endswith("n't") and not (word.equals("can't") or word.startswith("won't") or word.startswith("ain't")):
                    stress_pattern += utils.stressed + utils.unstressed
                else:
                    stress_pattern += utils.stressed

        stress_patterns.append(stress_pattern)

    return stress_patterns


def __count_syllables_in_word(word, dictionary):
    syllables = 0
    if word.startswith("'"):
        return syllables
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