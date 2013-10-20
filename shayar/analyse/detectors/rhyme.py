__author__ = 'Nitin'

import string
import nltk
from nltk.corpus import cmudict


def determine_rhyme_scheme(poem):
    last_words = []
    dictionary = cmudict.dict()
    for line in poem:
        exclude = set(string.punctuation)
        no_punct_line = ''.join(char for char in line if char not in exclude)
        tokenized_line = nltk.Text(nltk.word_tokenize(no_punct_line))
        last_word = tokenized_line[-1].lower()
        last_words.append(dictionary[last_word])

    return __get_rhyme_scheme(last_words)


def detect_internal_rhyme(poem):
    rhyme_scheme = []
    words = []
    dictionary = cmudict.dict()
    poem_end = False
    while not poem_end:
        for line in poem:
            if line.isspace:
                poem_end = line == poem[-1]
                break
            exclude = set(string.punctuation)
            no_punct_line = ''.join(char for char in line if char not in exclude)
            tokenized_line = nltk.Text(nltk.word_tokenize(no_punct_line))
            line_words = [w.lower() for w in tokenized_line]
            for word in line_words:
                try:
                    arpabet_word = dictionary[word]
                    words.append(arpabet_word)
                except KeyError:
                    continue
        rhyme_scheme.append(__get_rhyme_scheme(words))

    return rhyme_scheme


def __get_rhyme_scheme(words):
    rhyme_scheme_map = {}
    rhyme_scheme = []
    line_rhyme_token = 'A'
    for pronunciations in words:
        rhyme_tokens = []
        for pronunciation in pronunciations:
            index = 0
            for phoneme in pronunciation:
                if str(phoneme[-1]).isdigit() and str(phoneme[-1]) == "1":
                    if not str(pronunciation[index:]) in rhyme_scheme_map:
                        rhyme_scheme_map[str(pronunciation[index:])] = line_rhyme_token
                        line_rhyme_token = chr(ord(line_rhyme_token)+1)
                    rhyme_tokens.append(rhyme_scheme_map[str(pronunciation[index:])])
                index += 1

        rhyme_tokens = list(set(rhyme_tokens))
        if len(rhyme_tokens) == 1:
            rhyme_scheme.append(rhyme_tokens[0])
        else:
            rhyme_scheme.append(rhyme_tokens)

    return rhyme_scheme