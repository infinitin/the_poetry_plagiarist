__author__ = 'Nitin'

from nltk.corpus import cmudict
import string
import nltk
from difflib import get_close_matches
from itertools import product
import re
import csv

ono_type_map = {}


def set_up_globals():
    global dictionary
    dictionary = cmudict.dict()
    global stressed
    stressed = "1"
    global unstressed
    unstressed = "0"
    setup_ono_type_map()


def setup_ono_type_map():
    f = open('ono.csv', 'rb')
    reader = csv.reader(f)
    for row in reader:
        ono_type_map[row[0]] = str(row[1:]).strip('[]')
    f.close()

    return ono_type_map

def get_stanzas(poem):
    stanzas = []
    stanza = []
    for line in poem:
        if not line.strip():
            stanzas.append(stanza)
            stanza = []
        else:
            stanza.append(line)
    stanzas.append(stanza)
    return stanzas


# Remove the apostrophe and hyphen because they are legal letters in words for the the cmudict.
# Add them back in as spaces to separate the parts of the word in prep for cmudict.
def get_tokenized_words(line):
    exclude = set(string.punctuation)
    exclude.remove("'")
    exclude.remove("-")

    no_punct_line = ''.join(char for char in line if char not in exclude)
    no_punct_line = no_punct_line.replace(" '", " ")
    no_punct_line = no_punct_line.replace("-", " ")

    tokenized_line = nltk.Text(nltk.word_tokenize(no_punct_line))
    return [w.lower() for w in tokenized_line]


def get_pronunciations(word):
    try:
        pronunciations = dictionary[word]
    except KeyError:
        #Fuzzy matching on words to find closest
        pronunciations = dictionary[get_close_matches(word, cmudict.words(), 1)[0]]
        #Other options to make this more accurate:
            #Break many syllable words into likely part-words
            #Try all combos (stress/syllables only)
            #Add from shakespeare sonnets
            #Add from limericks
            #Add manually
        #Could also bias this for fewer changes near the end of the word for the sake of rhyme only.

    return pronunciations


def get_line_permutations(line):
    words = get_tokenized_words(line)
    pronunciations = [get_pronunciations(word) for word in words]
    return list(product(*pronunciations))


# Extends the likely pronunciations so that single syllable words can be either stressed or unstressed
# or if the word has a "light stress" (2) we treat it as either
def get_extended_line_permutations(line):
    words = get_tokenized_words(line)
    line_pronunciations = [get_pronunciations(word) for word in words]

    extended_pronunciations = []
    for word_pronunciations in line_pronunciations:
        extended_word_pronunciations = word_pronunciations

        for pronunciation in word_pronunciations:
            vowels = [phoneme for phoneme in pronunciation if str(phoneme[-1]).isdigit()]

            if len(vowels) == 1:
                alternate_stress_phoneme = vowels[0][:-1] + str(1 - int(vowels[0][-1]))
                new_pronunciation = [alternate_stress_phoneme if phoneme == vowels[0] else phoneme
                                     for phoneme in pronunciation]
                if not new_pronunciation in word_pronunciations:
                    extended_word_pronunciations.append(new_pronunciation)

            light_stresses = [vowel for vowel in vowels if str(vowel[-1]) == "2"]
            for light_stress in light_stresses:
                full_stress_phoneme = light_stress[:-1] + "1"
                no_stress_phoneme = light_stress[:-1] + "0"

                new_full_stress_pronunciation = [full_stress_phoneme if phoneme == light_stress else phoneme for
                                                 phoneme in pronunciation]
                new_no_stress_pronunciation = [no_stress_phoneme if phoneme == light_stress else phoneme for
                                               phoneme in pronunciation]

                if not new_full_stress_pronunciation in word_pronunciations:
                    extended_word_pronunciations.append(new_full_stress_pronunciation)
                if not new_no_stress_pronunciation in word_pronunciations:
                    extended_word_pronunciations.append(new_no_stress_pronunciation)

                extended_word_pronunciations = [x for x in extended_word_pronunciations if x != pronunciation]

        extended_pronunciations.append(extended_word_pronunciations)
    return list(product(*extended_pronunciations))


# Replace known abbreviations with the full form so that it gets picked up by cmudict.
# Can be removed by simply extending the cmudict.
def replace_contractions(line):
    replacement_patterns = [(r'won\'t', 'will not'),
                            (r'can\'t', 'cannot'),
                            (r'i\'m', 'i am'),
                            (r'ain\'t', 'is not'),
                            (r'(\w+)\'ll', '\g<1> will'),
                            (r'(\w+)n\'t', '\g<1> not'),
                            (r'(\w+)\'ve', '\g<1> have'),
                            (r'(\w+t)\'s', '\g<1> is'),
                            (r'(\w+)\'re', '\g<1> are'),
                            (r'(\w+)\'d', '\g<1> would'),
                            (r'(\w+)\'st', '\g<1>')]
    expanded_line = line
    patterns = [(re.compile(regex), expansion) for (regex, expansion) in replacement_patterns]
    for (pattern, expansion) in patterns:
        (expanded_line, count) = re.subn(pattern, expansion, expanded_line)
    return expanded_line