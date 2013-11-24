__author__ = 'Nitin'

from nltk.corpus import cmudict
import string
import nltk
from difflib import get_close_matches
from itertools import product


def set_up_globals():
    global dictionary
    dictionary = cmudict.dict()
    global stressed
    stressed = "1"
    global unstressed
    unstressed = "0"


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
