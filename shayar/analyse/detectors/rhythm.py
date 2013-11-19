__author__ = 'Nitin'

from utils import get_stanzas
import utils
from utils import get_tokenized_words


def count_syllables(poem):
    stanzas = get_stanzas(poem)
    syllabic_stanza_lengths = []

    for stanza in stanzas:
        syllabic_line_lengths = []

        for line in stanza:
            words = get_tokenized_words(line)

            syllabic_line_length = 0
            for word in words:
                syllabic_line_length += __count_syllables_in_word(word, utils.dictionary)

            syllabic_line_lengths.append(syllabic_line_length)

        syllabic_stanza_lengths.append(syllabic_line_lengths)

    return syllabic_stanza_lengths


def get_stress_pattern(poem):
    stress_patterns = []

    for line in poem:
        words = get_tokenized_words(line)

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