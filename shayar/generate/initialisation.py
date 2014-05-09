__author__ = 'Nitin'
import random


def init_poem(settings):
    stanzas = random.choice(settings["stanzas"])
    distinct_sentences = list(random.choice(settings["distinct_sentences"]))
    lines = list(random.choice(settings["num_lines"]))

    tenses = list(random.choice(settings["line_tenses"]))
    modality_by_line = random.choice(settings(["modality_by_line"]))
    mood_by_line = random.choice(settings(["mood_by_line"]))
    subjectivity_by_line = random.choice(settings(["subjectivity_by_line"]))
    polarity_by_line = random.choice(settings(["polarity_by_line"]))
    

#syllabic rhythm
#Rhyme scheme
#Stress patterns for each line

#Number and positions of repeated lines
#Common n grams
