from __future__ import division
__author__ = 'Nitin'


from utils import get_line_permutations


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
    patterns = []

    for line in poem:
        phoneme_set = __get_start_or_stressed_phonemes(line) if alliteration else __get_phonemes(line, consonance)
        line_patterns = {}
        for phonemes in phoneme_set:
            multiple = [phoneme for phoneme in phonemes if phonemes.count(phoneme) >= 2 and phoneme]
            for phoneme in multiple:
                line_patterns[phoneme] = phonemes.count(phoneme)

        total = 0
        for occurrence in line_patterns.values():
            total += occurrence

        if total > 2:
            patterns.append(line_patterns)
        else:
            patterns.append({})

    return patterns


# Get the phonemes of all different pronunciations in the line
# If is_consonant is true then we only grab the consonant phonemes, otherwise we grab the vowels phonemes
def __get_phonemes(line, is_consonant):
    line_permutations = get_line_permutations(line)

    phoneme_set = []
    for line_permutation in line_permutations:

        phonemes = []
        for pronunciation in line_permutation:
            if is_consonant:
                phonemes.extend([phoneme for phoneme in pronunciation if not str(phoneme[-1]).isdigit()])
            else:
                phonemes.extend([phoneme for phoneme in pronunciation if str(phoneme[-1]).isdigit()])

        phoneme_set.append(phonemes)

    #Return unique elements
    return [list(x) for x in set(tuple(x) for x in phoneme_set)]


# Alliteration occurs when consonants are repeated at the beginning or on the stressed syllable of consecutive words.
# So this grabs the stressed consonant or otherwise the first consonant of each word in the line.
def __get_start_or_stressed_phonemes(line):
    line_permutations = get_line_permutations(line)

    phoneme_set = []
    for line_permutation in line_permutations:

        phonemes = []
        for pronunciation in line_permutation:

            previous_phoneme = ""
            first_found = False
            for phoneme in pronunciation:
                if not str(phoneme[-1]).isdigit():
                    if not first_found:
                        phonemes.append(phoneme)
                        first_found = True
                    else:
                        previous_phoneme = phoneme
                else:
                    if str(phoneme[-1]) == '1':
                        phonemes.append(previous_phoneme)
        phoneme_set.append(phonemes)

    #Return unique elements
    return [list(x) for x in set(tuple(x) for x in phoneme_set)]





