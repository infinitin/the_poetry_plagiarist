__author__ = 'Nitin'
from shayar.analyse.detectors.rhythm import get_stress_pattern, count_syllables
import builder
from framenet_reader import get_random_word
import random
import phrase_spec
from operator import itemgetter
from pattern.text.en import lemma


def fit_rhythm_pattern(phrases, pattern):
    #phrases = fit_pattern(fit_syllables(phrases, len(pattern)), pattern)
    phrases = fit_syllables(phrases, len(pattern))
    return [phrase for phrase in phrases if phrase is not None]


#First get the number of syllables right
def fit_syllables(phrases, target_num_syllables):
    line = builder.make_clause(phrases)
    #Get the realisation
    realisation = builder.realiser.realise(line).getRealisation()

    #Count the syllables
    num_syllables = count_syllables([realisation])[0]

    if num_syllables < target_num_syllables:
        return extend_phrase(phrases, target_num_syllables, num_syllables)
    elif num_syllables > target_num_syllables:
        return reduce_phrase(phrases, target_num_syllables, num_syllables)
    else:
        return phrases


def reduce_phrase(phrases, target_num_syllables, num_syllables):
    try_num = 10
    for phrase in phrases:
        phrase.modifiers = []
        phrase.complements = []
        if 'np' in phrase.__dict__.keys():
            phrase.np.modifiers = []
            phrase.np.complements = []

    total_tries = try_num*2
    new_phrases = phrases
    line = builder.make_clause(phrases)
    realisation = str(builder.realiser.realise(line).getRealisation())
    while target_num_syllables < num_syllables and total_tries:
        phrases = new_phrases
        new_phrases = []
        split_realisation = [[word] for word in realisation.split()]
        syllables_for_each_word = zip(realisation.split(), count_syllables(split_realisation))
        longest_word = max(syllables_for_each_word, key=itemgetter(1))
        for phrase in phrases:
            if 'noun' in phrase.__dict__.keys():
                if phrase.noun == lemma(longest_word[0]):
                    tries = try_num
                    while len(phrase.stress_patterns[0]) >= longest_word[1] and tries:
                        phrase = phrase_spec.NP(get_random_word('N'))
                        tries -= 1

            elif 'verb' in phrase.__dict__.keys():
                if phrase.verb == lemma(longest_word[0]):
                    tries = try_num
                    while len(phrase.stress_patterns[0]) >= longest_word[1] and tries:
                        phrase = phrase_spec.VP(get_random_word('V'))
                        tries -= 1

            elif 'np' in phrase.__dict__.keys():
                if phrase.np.noun == lemma(longest_word[0]):
                    tries = try_num
                    while len(phrase.np.stress_patterns[0]) >= longest_word[1] and tries:
                        phrase.np = phrase_spec.NP(get_random_word('N'))
                        tries -= 1

            new_phrases.append(phrase)

        total_tries -= 1
        line = builder.make_clause(new_phrases)
        realisation = str(builder.realiser.realise(line).getRealisation())
        num_syllables = count_syllables([realisation])[0]

    if not new_phrases:
        new_phrases = phrases

    if num_syllables < target_num_syllables:
        return extend_phrase(new_phrases, target_num_syllables, num_syllables)
    else:
        return new_phrases


def extend_phrase(phrases, target_num_syllables, num_syllables):
    #While less than:
    #Add adjectives and adverbs as modifiers with max missing number of syllables
    while num_syllables < target_num_syllables:
        phrase_to_change = phrases.index(random.choice(phrases))
        pos = 'A'
        if 'verb' in phrases[phrase_to_change].__dict__.keys():
            pos = 'AVP'

        #Need to check that it is <= the required number of syllables
        word = ''
        added_syllables = 0
        tries = 10
        while tries:
            word = get_random_word(pos)
            added_syllables = count_syllables([word])[0]
            if added_syllables <= (target_num_syllables - num_syllables):
                break
            tries -= 1

        if pos == 'A':
            modifier_phrase = phrase_spec.ADJ(word)
        else:
            modifier_phrase = phrase_spec.ADV(word)

        phrases[phrase_to_change].modifiers.append(modifier_phrase)

        num_syllables += added_syllables

    return phrases


#Now that we have the right number of syllables, fix the sentence so that it matches the rhythm patterns
#Replace words that don't match the rhythm for their position
def fit_pattern(phrases, pattern):
    new_phrases = []
    line = builder.make_clause(phrases)
    #Find the stress pattern of each individual word
    words = builder.realiser.realise(line).getRealisation().split()
    stress_patterns = get_stress_pattern(builder.realiser.realise(line).getRealisation().split())
    stress_patterns = zip(words, stress_patterns)

    #If it does not match the given pattern for its position, add it to a 'replace' list, with the required pattern
    to_be_replaced = []
    for word, patterns in stress_patterns:
        word_len = len(patterns[0])     # FIXME: Some words have multiple syllable lengths e.g. towards
        required = pattern[:word_len]

        if not required in patterns:
            replace = (word, required)
            to_be_replaced.append(replace)

        pattern = pattern[word_len:]

    #Find synonyms for those in the replace list, replace directly and return
    for word, required in to_be_replaced:
        #Find the word among the phrases
        #Replace with different word with same pos and required pattern
        for phrase in phrases:
            if 'noun' in phrase.__dict__.keys():
                if phrase.noun == word:
                    tries = 10
                    while required not in get_stress_pattern(phrase.noun) and tries:
                        phrase = phrase_spec.NP(get_random_word('N'))
                        tries -= 1

            if 'verb' in phrase.__dict__.keys():
                if phrase.verb == word:
                    tries = 10
                    while required not in get_stress_pattern(phrase.noun) and tries:
                        phrase = phrase_spec.VP(get_random_word('V'))
                        tries -= 1

            if 'np' in phrase.__dict__.keys():
                if phrase.np.noun == word:
                    tries = 10
                    while required not in get_stress_pattern(phrase.np .noun) and tries:
                        phrase.np = phrase_spec.NP(get_random_word('N'))
                        tries -= 1

            for modifier in phrase.modifiers:
                if 'adjective' in modifier.__dict__.keys():
                    if modifier.adjective == word:
                        new_modifier = modifier
                        tries = 10
                        while required not in get_stress_pattern(new_modifier.adjective) and tries:
                            new_modifier = phrase_spec.ADJ(get_random_word('A'))
                            tries -= 1
                        if tries:
                            modifier_index = phrase.modifiers.index(modifier)
                            phrase.modifiers[modifier_index] = new_modifier
                if 'adverb' in modifier.__dict__.keys():
                    if modifier.adverb == word:
                        new_modifier = modifier
                        tries = 10
                        while required not in get_stress_pattern(new_modifier.adverb) and tries:
                            new_modifier = phrase_spec.ADV(get_random_word('AVP'))
                            tries -= 1
                        if tries:
                            modifier_index = phrase.modifiers.index(modifier)
                            phrase.modifiers[modifier_index] = new_modifier

            new_phrases.append(phrase)

    if not new_phrases:
        new_phrases = phrases

    return new_phrases