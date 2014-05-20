__author__ = 'Nitin'
from shayar.analyse.detectors.rhythm import get_stress_pattern, count_syllables
import builder
from framenet_reader import get_random_word
import random


def fit_rhythm_pattern(line, phrases, pattern):
    return fit_pattern(fit_syllables(line, phrases, len(pattern)), phrases, pattern)


def fit_syllables(line, phrases, target_num_syllables):
    #Get the realisation
    realisation = builder.realiser.realise(line).getRealisation()

    #Count the syllables
    num_syllables = count_syllables([realisation])[0]

    #While less than:
        #Add adjectives and adverbs as modifiers with max missing number of syllables
    while num_syllables < target_num_syllables:
        pos = random.choice(['A', 'AVP'])
        word = get_random_word(pos)
        phrase_to_change = None
        if pos == 'A':
            #Add it as a modifier to one of the noun/prep phrases
            phrase_to_change = [phrases.index(phrase) for phrase in phrases if phrase[1] == 'P' or phrase[1] == 'N']
        elif pos == 'AVP':
            #Add it as a modifier to one of the verb phrases
            phrase_to_change = [phrases.index(phrase) for phrase in phrases if phrase[1] == 'V' or phrase[1] == 'A']

        phrases[random.choice(phrase_to_change)].addModifier(word)

    return builder.make_clause(phrases)


def fit_pattern(line, pattern):
    #Find the stress pattern of each individual word
    #If it does not match the given pattern for its position, add it to a 'replace' list, with the required pattern

    #Find synonyms for those in the replace list, replace directly and return
    pass