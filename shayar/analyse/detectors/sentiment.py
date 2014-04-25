__author__ = 'Nitin'
from pattern.text.en import sentiment, modality, parse, Sentence, mood


def get_sentiment_by_line(poem):
    return [sentiment(line) for line in poem]


def get_modality_by_line(poem):
    return [round(modality(Sentence(parse(line, lemmata=True))), 1) for line in poem]


def get_mood_by_line(poem):
    return [mood(Sentence(parse(line, lemmata=True))) for line in poem]