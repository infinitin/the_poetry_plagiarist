__author__ = 'Nitin'
from pattern.text.en import sentiment, modality, parse, Sentence


def get_sentiment_by_line(poem):
    return [round(sentiment(line)) for line in poem]


def get_modality_by_line(poem):
    return [round(modality(Sentence(parse(line, lemmata=True)))) for line in poem]