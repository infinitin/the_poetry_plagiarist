__author__ = 'Nitin'

from pattern.text.en import parsetree
from utils import get_tokenized_words

#Looks at PP chunks to see if certain simile words are present.
#Can be improved by checking that an adjective precedes an 'as' or 'than' simile
#  and a verb precedes a 'like' simile
def detect_simile(poem):
    full = ""

    for line in poem:
        full += line + " "

    s = parsetree(full, relations=True)

    similes = []
    simile_words = {'like', 'as', 'than', 'to'}
    for sentence in s.sentences:
        for pnp_chunk in sentence.pnp:
            words = set(pnp_chunk.string.split(" "))
            if list(words & simile_words) and valid_simile_structure(sentence.string, list(words & simile_words)):
                    similes.append(sentence.string)

    return similes


def valid_simile_structure(sentence, simile_words):

    if 'like' in simile_words:
        s = parsetree(sentence[:sentence.index('like')], relations=True)
        if s.sentences[0].verbs:
            return True

    if 'as' in simile_words:
        s = parsetree(sentence[:sentence.rfind('as')], relations=True)
        for word in s.sentences[0]:
            if word.type.startswith('J'):
                return True
    elif 'than' in simile_words:
        s = parsetree(sentence[:sentence.index('than')], relations=True)
        for word in s.sentences[0]:
            if word.type.startswith('J'):
                return True

    return False

