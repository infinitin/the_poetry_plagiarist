__author__ = 'Nitin'
from shayar.analyse.detectors.rhythm import get_stress_pattern, count_syllables
from framenet_reader import get_random_word, filter_candidates
import random
import phrase_spec
from operator import itemgetter
from pattern.text.en import lemma
import creation
import builder
from urllib2 import urlopen, URLError
from json import loads as json_load
from pattern.text.en import wordnet
from shayar.knowledge.knowledge import get_property, most_similar, get_synonyms, get_node, closest_matching, halo
import logging
import sys


def fit_rhythm_pattern(phrases, pattern):
    #phrases = fit_pattern(fit_syllables(phrases, len(pattern)), pattern)
    phrases = fit_syllables(phrases, len(pattern))
    return [phrase for phrase in phrases if phrase is not None]


#First get the number of syllables right
def fit_syllables(phrases, target_num_syllables):
    logging.info('Rephrasing to fit rhythm')
    line = builder.make_clause(phrases)
    #Get the realisation
    realisation = creation.realiser.realise(line).getRealisation()

    #Count the syllables
    num_syllables = count_syllables([realisation])[0]

    if num_syllables < target_num_syllables:
        return extend_phrase(phrases, target_num_syllables, num_syllables)
    #elif num_syllables > target_num_syllables:
    #    return reduce_phrase(phrases, target_num_syllables, num_syllables)
    else:
        return phrases


def reduce_phrase(phrases, target_num_syllables, num_syllables):
    logging.info('Reducing Phrase')

    try_num = 10
    total_tries = try_num * 2
    new_phrases = phrases
    line = builder.make_clause(phrases)
    realisation = str(creation.realiser.realise(line).getRealisation())
    while target_num_syllables < num_syllables and total_tries:
        phrases = new_phrases
        new_phrases = []
        split_realisation = [[word] for word in realisation.split()]
        syllables_for_each_word = zip(realisation.split(), count_syllables(split_realisation))
        longest_word = max(syllables_for_each_word, key=itemgetter(1))
        for phrase in phrases[:-1]:
            if 'noun' in phrase.__dict__.keys():
                if phrase.noun == lemma(longest_word[0]):
                    tries = try_num
                    while phrase.stress_patterns and len(phrase.stress_patterns[0]) >= longest_word[1] and tries:
                        phrase = phrase_spec.NP(get_random_word('N'))
                        tries -= 1

            elif 'verb' in phrase.__dict__.keys():
                if phrase.verb == lemma(longest_word[0]):
                    tries = try_num
                    while phrase.stress_patterns and len(phrase.stress_patterns[0]) >= longest_word[1] and tries:
                        phrase = phrase_spec.VP(get_random_word('V'))
                        tries -= 1

            elif 'np' in phrase.__dict__.keys():
                if phrase.np.noun == lemma(longest_word[0]):
                    tries = try_num
                    while phrase.stress_patterns and len(phrase.np.stress_patterns[0]) >= longest_word[1] and tries:
                        phrase.np = phrase_spec.NP(get_random_word('N'))
                        tries -= 1

            new_phrases.append(phrase)

        new_phrases.append(phrases[-1:][0])
        total_tries -= 1
        line = builder.make_clause(new_phrases)
        realisation = str(creation.realiser.realise(line).getRealisation())
        num_syllables = count_syllables([realisation])[0]

    if not new_phrases:
        new_phrases = phrases

    if num_syllables < target_num_syllables:
        return extend_phrase(new_phrases, target_num_syllables, num_syllables)
    else:
        return new_phrases


def extend_phrase(phrases, target_num_syllables, num_syllables):
    logging.info('Extending phrase')
    used = []
    #While less than:
    #Add adjectives and adverbs as modifiers with max missing number of syllables
    while num_syllables < target_num_syllables:
        added_specifier = False
        if target_num_syllables == num_syllables + 1:
            for phrase in phrases:
                if 'noun' in phrase.__dict__.keys():
                    if phrase.specifier is None:
                        phrase.specifier = 'the'
                        added_specifier = True
                        break
                elif 'np' in phrase.__dict__.keys():
                    if phrase.np.specifier is None:
                        phrase.np.specifier = 'the'
                        added_specifier = True
                        break
            if added_specifier:
                break
        if added_specifier:
            break

        changeable_phrases = []
        for phrase in phrases:
            try:
                if 'noun' in phrase.__dict__.keys() and phrase.noun[0].isupper():
                    continue
                else:
                    changeable_phrases.append(phrase)
            except IndexError:
                changeable_phrases.append(phrase)

        phrase_to_change = phrases.index(random.choice(changeable_phrases))
        pos = 'A'
        target_pos = 'N'
        if 'verb' in phrases[phrase_to_change].__dict__.keys():
            target_word = phrases[phrase_to_change].verb
            target_pos = 'V'
            pos = 'AVP'
        elif 'np' in phrases[phrase_to_change].__dict__.keys():
            target_word = phrases[phrase_to_change].np.noun
        else:
            target_word = phrases[phrase_to_change].noun

        #Need to check that it is <= the required number of syllables
        word = ''
        added_syllables = 0
        tries = 10
        while tries:
            try:
                word = get_property(lemma(target_word.split()[-1]), target_pos, used)
            except IndexError:
                word = get_random_word(pos)

            used.append(word)
            added_syllables = count_syllables([word])[0]
            if added_syllables <= (target_num_syllables - num_syllables):
                break
            tries -= 1

        if pos == 'A':
            modifier_phrase = phrase_spec.ADJ(word)
        else:
            modifier_phrase = phrase_spec.ADV(word)

        phrases[phrase_to_change].pre_modifiers.append(modifier_phrase)

        num_syllables += added_syllables

    return phrases


#Now that we have the right number of syllables, fix the sentence so that it matches the rhythm patterns
#Replace words that don't match the rhythm for their position
def fit_pattern(phrases, pattern):
    new_phrases = []
    line = builder.make_clause(phrases)
    #Find the stress pattern of each individual word
    words = creation.realiser.realise(line).getRealisation().split()
    stress_patterns = get_stress_pattern(creation.realiser.realise(line).getRealisation().split())
    stress_patterns = zip(words, stress_patterns)

    #If it does not match the given pattern for its position, add it to a 'replace' list, with the required pattern
    to_be_replaced = []
    for word, patterns in stress_patterns:
        word_len = len(patterns[0])  # FIXME: Some words have multiple syllable lengths e.g. towards
        required = pattern[:word_len]

        if not required in patterns:
            replacement = (word, required)
            to_be_replaced.append(replacement)

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
                    while required not in get_stress_pattern(phrase.np.noun) and tries:
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


def fit_rhyme(phrases, rhyme_token):
    logging.info('Rephrasing to fit rhyme')
    line = builder.make_clause(phrases)
    last_word = creation.realiser.realise(line).getRealisation().split()[-1]

    if not creation.rhyme_scheme[rhyme_token]:
        creation.rhyme_scheme[rhyme_token] = [last_word.lower()]
        print last_word
        return phrases

    rhyme_word = creation.rhyme_scheme[rhyme_token][0]
    rhymes = get_rhymes(rhyme_word)
    if rhymes:
        candidates = [entry for entry in rhymes if
                      entry['word'] not in creation.rhyme_scheme[rhyme_token] and entry['score'] >= 300]
        if not candidates:
            candidates = [entry for entry in rhymes if
                          entry['word'] not in creation.rhyme_scheme[rhyme_token] and entry['score'] >= 250]
        if not candidates:
            short_rhyme_word = shorten(rhyme_word)
            if short_rhyme_word and short_rhyme_word != 'ed' and short_rhyme_word != 'tion':
                rhymes.extend(get_rhymes(short_rhyme_word))
            candidates = [entry for entry in rhymes if
                          entry['word'] not in creation.rhyme_scheme[rhyme_token] and entry['score'] >= 300]
        if not candidates:
            candidates = [entry for entry in rhymes if
                          entry['word'] not in creation.rhyme_scheme[rhyme_token] and entry['score'] >= 250]
        if not candidates:
            candidates = [entry for entry in rhymes if
                          entry['word'] not in creation.rhyme_scheme[rhyme_token] and entry['score'] >= 200]
        if not candidates:
            candidates = rhymes

        #Send to replace function
        phrases = replace(last_word, candidates, phrases)

        new_line = builder.make_clause(phrases)

        chosen = creation.realiser.realise(new_line).getRealisation().split()[-1]
        creation.rhyme_scheme[rhyme_token].append(chosen.lower())
        print chosen

    return phrases


def shorten(word):
    found = False
    for letter in word[::-1]:
        if letter in 'aeiou' and found:
            vowel_index = word.rindex(letter)
            if vowel_index == 0:
                return ''
            elif word[vowel_index - 1] not in 'aeiou':
                return word[vowel_index - 1:]
        elif letter not in 'aeiou':
            found = True
    return ''


def get_rhymes(rhyme_word):
    #Make an API request to RhymeBrain in JSON form
    url = "http://rhymebrain.com/talk?function=getRhymes&lang=en&word="
    request_url = url + rhyme_word
    try:
        socket = urlopen(request_url)
        json = json_load(socket.read())
        socket.close()
    except URLError:
        raise Exception("You are not connected to the Internet!")

    return json


def replace(old_word, candidates, phrases):
    new_phrases = []
    #Find the word among the phrases, replace with candidate with same pos
    for phrase in phrases:
        if 'noun' in phrase.__dict__.keys():
            if phrase.noun == lemma(old_word):
                replacement = get_rhyme_word(old_word, candidates, 'N')
                if not replacement:
                    phrase.post_modifiers.append(phrase_spec.ADJ(get_rhyme_mod(old_word, candidates, 'A', 'N')))
                else:
                    phrase = phrase_spec.NP(replacement)

        if 'verb' in phrase.__dict__.keys():
            if phrase.verb == lemma(old_word):
                replacement = get_rhyme_word(old_word, candidates, 'V')
                if not replacement:
                    phrase.post_modifiers.append(phrase_spec.ADV(get_rhyme_mod(old_word, candidates, 'AVP', 'V')))
                else:
                    phrase = phrase_spec.VP(replacement)

        if 'np' in phrase.__dict__.keys():
            if phrase.np.noun == lemma(old_word):
                replacement = get_rhyme_word(old_word, candidates, 'N')
                if not replacement:
                    phrase.np.post_modifiers.append(
                        phrase_spec.ADJ(get_rhyme_mod(old_word, candidates, 'A', 'N')))
                else:
                    phrase.np = phrase_spec.NP(replacement)

        for pre_modifier in phrase.pre_modifiers:
            if 'adjective' in pre_modifier.__dict__.keys():
                if pre_modifier.adjective == lemma(old_word):
                    option_nodes = [get_node(candidate['word'], 'a') for candidate in candidates]
                    replacement_nodes = list(closest_matching([get_node(old_word, 'a')], option_nodes))
                    if replacement_nodes:
                        replacement = random.choice(replacement_nodes).id.split()[0]
                    else:
                        replacement = random.choice(candidates)['word']
                    new_pre_modifier = phrase_spec.ADJ(replacement)
                    pre_modifier_index = phrase.pre_modifiers.index(pre_modifier)
                    phrase.pre_modifiers[pre_modifier_index] = new_pre_modifier
            if 'adverb' in pre_modifier.__dict__.keys():
                if pre_modifier.adverb == lemma(old_word):
                    option_nodes = [get_node(candidate['word'], 'adv') for candidate in candidates]
                    replacement_nodes = list(closest_matching([get_node(old_word, 'adv')], option_nodes))
                    if replacement_nodes:
                        replacement = random.choice(replacement_nodes).id.split()[0]
                    else:
                        replacement = random.choice(candidates)['word']
                    new_pre_modifier = phrase_spec.ADJ(replacement)
                    pre_modifier_index = phrase.pre_modifiers.index(pre_modifier)
                    phrase.pre_modifiers[pre_modifier_index] = new_pre_modifier

        for modifier in phrase.modifiers:
            if 'adjective' in modifier.__dict__.keys():
                if modifier.adjective == lemma(old_word):
                    option_nodes = [get_node(candidate['word'], 'a') for candidate in candidates]
                    replacement_nodes = list(closest_matching([get_node(old_word, 'a')], option_nodes))
                    if replacement_nodes:
                        replacement = random.choice(replacement_nodes).id.split()[0]
                    else:
                        replacement = random.choice(candidates)['word']
                    new_modifier = phrase_spec.ADJ(replacement)
                    modifier_index = phrase.modifiers.index(modifier)
                    phrase.modifiers[modifier_index] = new_modifier
            if 'adverb' in modifier.__dict__.keys():
                if modifier.adverb == lemma(old_word):
                    option_nodes = [get_node(candidate['word'], 'adv') for candidate in candidates]
                    replacement_nodes = list(closest_matching([get_node(old_word, 'adv')], option_nodes))
                    if replacement_nodes:
                        replacement = random.choice(replacement_nodes).id.split()[0]
                    else:
                        replacement = random.choice(candidates)['word']
                    new_modifier = phrase_spec.ADJ(replacement)
                    modifier_index = phrase.modifiers.index(modifier)
                    phrase.modifiers[modifier_index] = new_modifier

        for post_modifier in phrase.post_modifiers:
            if 'adjective' in post_modifier.__dict__.keys():
                if post_modifier.adjective == lemma(old_word):
                    option_nodes = [get_node(candidate['word'], 'a') for candidate in candidates]
                    replacement_nodes = list(closest_matching([get_node(old_word, 'a')], option_nodes))
                    if replacement_nodes:
                        replacement = random.choice(replacement_nodes).id.split()[0]
                    else:
                        replacement = random.choice(candidates)['word']
                    new_post_modifier = phrase_spec.ADJ(replacement)
                    post_modifier_index = phrase.post_modifiers.index(post_modifier)
                    phrase.post_modifiers[post_modifier_index] = new_post_modifier
            if 'adverb' in post_modifier.__dict__.keys():
                if post_modifier.adverb == lemma(old_word):
                    option_nodes = [get_node(candidate['word'], 'adv') for candidate in candidates]
                    replacement_nodes = list(closest_matching([get_node(old_word, 'adv')], option_nodes))
                    if replacement_nodes:
                        replacement = random.choice(replacement_nodes).id.split()[0]
                    else:
                        replacement = random.choice(candidates)['word']
                    new_post_modifier = phrase_spec.ADJ(replacement)
                    post_modifier_index = phrase.post_modifiers.index(post_modifier)
                    phrase.post_modifiers[post_modifier_index] = new_post_modifier

        new_phrases.append(phrase)

    if not new_phrases:
        new_phrases = phrases

    return new_phrases


def get_rhyme_mod(word, candidates, mod_pos, pos):
    #Find the candidates in the lexicon
    words = [candidate['word'] for candidate in candidates]
    filtered = filter_candidates(words, mod_pos)
    options = [candidate for candidate in candidates if candidate['word'] in filtered]

    if len(filtered) == 1:
        return options[0]['word']

    if not options:
        best_options = [candidate['word'] for candidate in candidates if candidate['score'] == candidates[0]['score']]
    else:
        best_options = [option['word'] for option in options if option['score'] == options[0]['score']]

    if len(best_options) == 1:
        return best_options[0]

    wpos = wordnet.NOUN
    if pos.startswith('V'):
        wpos = wordnet.VERB

    #Which modifier is most similar to those that are used to describe any of these words (synonyms)
    synonyms = get_synonyms(word, wpos)
    properties = []
    for target_word in synonyms:
        target_node = get_node(target_word, pos.lower())
        if target_node is not None:
            properties.extend(halo(target_node, relation='HasProperty'))

    closest = closest_matching([get_node(option, mod_pos.lower()) for option in best_options], properties)
    if closest:
        best_closest = random.choice(list(closest)).id.split('.')[0]
    else:
        best_closest = random.choice(best_options)

    return best_closest


def get_rhyme_word(old_word, candidates, pos):
    #Find the candidates in the lexicon
    lemmas = [lemma(candidate['word']) for candidate in candidates]
    filtered_lemmas = filter_candidates(lemmas, pos)
    options = [candidate for candidate in candidates if lemma(candidate['word']) in filtered_lemmas]

    if not options:
        return ''

    best_options = [option['word'] for option in options if option['score'] == options[0]['score']]

    closest, score = most_similar(old_word, best_options, pos)
    if score > 2.5:
        return ''

    return closest


#Return the word in candidates that is closest to an option compared to any other candidate-option pair
def most_similar_pair(options, candidates, pos):
    best_closest = random.choice(candidates)
    best_score = sys.maxint
    for option in options:
        closest, score = most_similar(option, candidates, pos)
        if score < best_score:
            best_score = score
            best_closest = closest

    return best_closest