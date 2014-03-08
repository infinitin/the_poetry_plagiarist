__author__ = 'Nitin'

from utils import get_stanzas
from utils import get_tokenized_words
from utils import get_pronunciations
from utils import get_extended_line_permutations


# Stress pattern is done by stripping out the digit of each vowel
# We append to a string so that we can use fuzzy string comparison algorithms like Jaro-Winkler
# Words with apostrophes cause problems.
# Words that are not in cmudict also cause problems. Need to expand cmudict as much as possible through learning.
def get_stress_pattern(poem):
    stress_patterns = []

    for line in poem:
        line_permutations = get_extended_line_permutations(line)
        line_stress_patterns = set()
        for line_permutation in line_permutations:
            stress_pattern = ""
            for pronunciation in line_permutation:
                for phoneme in pronunciation:
                    if str(phoneme[-1]).isdigit():
                        stress_pattern += str(phoneme[-1])
            if not '111' in stress_pattern and not '000' in stress_pattern:
                line_stress_patterns.add(stress_pattern)

        stress_patterns.append(list(line_stress_patterns))

    return stress_patterns


# We want a list of of the syllable counts of each line as well as a pattern for each stanza
# This is because we may have an alternating pattern of syllabic rhythm
def count_syllables(poem):

    syllabic_line_lengths = []

    for line in poem:
        words = get_tokenized_words(line)

        syllabic_line_length = 0
        for word in words:
            syllabic_line_length += __count_syllables_in_word(word)

        syllabic_line_lengths.append(syllabic_line_length)

    return tuple(syllabic_line_lengths)


def __count_syllables_in_word(word):
    syllables = 0
    if word.startswith("'"):
        return syllables
    pronunciation = get_pronunciations(word)[0]
    for phoneme in pronunciation:
        if str(phoneme[-1]).isdigit():
            syllables += 1

    return syllables