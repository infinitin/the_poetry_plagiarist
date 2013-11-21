__author__ = 'Nitin'

from nltk.corpus import cmudict
import string
import nltk


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