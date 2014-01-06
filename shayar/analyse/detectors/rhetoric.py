__author__ = 'Nitin'

from pattern.text.en import parsetree, Chunk, PNPChunk


def detect_simile(poem):
    full = ""

    for line in poem:
        full += line + " "

    s = parsetree(full, relations=True)

    similes = []
    simile_words = set(['like', 'as', 'than', 'to'])
    for sentence in s.sentences:
        for pnp_chunk in sentence.pnp:
            words = set(pnp_chunk.string.split(" "))
            if list(words & simile_words):
                similes.append(sentence.string)

    return similes