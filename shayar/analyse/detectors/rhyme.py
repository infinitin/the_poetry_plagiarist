__author__ = 'Nitin'

from utils import get_stanzas
import utils
from utils import get_tokenized_words


def determine_rhyme_scheme(poem):
    stanzas = get_stanzas(poem)
    stanza_rhyme_scheme = []

    for stanza in stanzas:
        last_words = []

        for line in stanza:
            if line.strip():
                words = get_tokenized_words(line)
                last_word = words[-1]

                try:
                    last_words.append(utils.dictionary[last_word])
                except KeyError:
                    continue

        stanza_rhyme_scheme.append(__get_rhyme_scheme(last_words))

    return stanza_rhyme_scheme


def detect_internal_rhyme(poem):
    stanzas = get_stanzas(poem)
    rhyme_scheme = []

    for stanza in stanzas:
        words = []

        for line in stanza:
            line_words = get_tokenized_words(line)

            for word in line_words:
                try:
                    arpabet_word = utils.dictionary[word]
                    words.append(arpabet_word)
                except KeyError:
                    words.append('')
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
                if str(phoneme[-1]).isdigit() and str(phoneme[-1]) == utils.stressed:
                    rhyme_phonemes = __get_rhyme_phonemes(pronunciation[index:])

                    if not rhyme_phonemes in rhyme_scheme_map:
                        rhyme_scheme_map[rhyme_phonemes] = line_rhyme_token
                        line_rhyme_token = chr(ord(line_rhyme_token)+1)
                    else:
                        if phoneme == '':
                            rhyme_tokens.append(line_rhyme_token)
                            line_rhyme_token = chr(ord(line_rhyme_token)+1)

                    rhyme_tokens.append(rhyme_scheme_map[rhyme_phonemes])
                index += 1

        rhyme_tokens = list(set(rhyme_tokens))
        if len(rhyme_tokens) == 1:
            rhyme_scheme.append(rhyme_tokens[0])
        else:
            rhyme_scheme.append(rhyme_tokens)

    return rhyme_scheme


def __get_rhyme_phonemes(phonemes):
    rhyme_phonemes = []

    for phoneme in phonemes:
        if str(phoneme[-1]).isdigit() or phonemes[-1] == phoneme:
            rhyme_phonemes.append(phoneme)

    return str(rhyme_phonemes)
