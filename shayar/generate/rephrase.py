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
from pattern.text.en import wordnet, singularize
from pattern.text.en import lemma as lemmatise
import logging


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
    changable_phrases = phrases[:-1]
    used = []
    #While less than:
    #Add adjectives and adverbs as modifiers with max missing number of syllables
    while num_syllables < target_num_syllables:
        if target_num_syllables == num_syllables+1:
            added_specifier = False
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
        else:
            phrase_to_change = phrases.index(random.choice(changable_phrases))
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
                word = get_property(target_word, target_pos, used)
                used.append(word)
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
        creation.rhyme_scheme[rhyme_token] = [last_word]
        return phrases

    rhyme_word = creation.rhyme_scheme[rhyme_token][0]
    #Make an API request to RhymeBrain in JSON form
    url = "http://rhymebrain.com/talk?function=getRhymes&lang=en&word="
    request_url = url + rhyme_word
    try:
        socket = urlopen(request_url)
        json = json_load(socket.read())
        socket.close()
    except URLError:
        raise Exception("You are not connected to the Internet!")

    if json:
        candidates = [entry for entry in json if
                      entry['word'] not in creation.rhyme_scheme[rhyme_token] and entry['score'] >= 300]
        if not candidates:
            candidates = [entry for entry in json if
                          entry['word'] not in creation.rhyme_scheme[rhyme_token] and entry['score'] >= 250]
        if not candidates:
            candidates = json

        #Send to replace function
        phrases = replace(last_word, candidates, phrases)
        new_line = builder.make_clause(phrases)

        chosen = creation.realiser.realise(new_line).getRealisation().split()[-1]
        creation.rhyme_scheme[rhyme_token].append(chosen)

    return phrases


def replace(old_word, candidates, phrases):
    new_phrases = []
    #Find the word among the phrases, replace with candidate with same pos
    for phrase in phrases:
        if 'noun' in phrase.__dict__.keys():
            if phrase.noun == old_word:
                phrase = phrase_spec.NP(get_rhyme_word(old_word, candidates, 'N'))

        if 'verb' in phrase.__dict__.keys():
            if phrase.verb == old_word:
                phrase = phrase_spec.VP(get_rhyme_word(old_word, candidates, 'V'))

        if 'np' in phrase.__dict__.keys():
            if phrase.np.noun == old_word:
                phrase.np = phrase_spec.NP(get_rhyme_word(old_word, candidates, 'N'))

        for modifier in phrase.modifiers:
            if 'adjective' in modifier.__dict__.keys():
                if modifier.adjective == old_word:
                    new_modifier = phrase_spec.ADJ(get_rhyme_word(old_word, candidates, 'A'))
                    modifier_index = phrase.modifiers.index(modifier)
                    phrase.modifiers[modifier_index] = new_modifier
            if 'adverb' in modifier.__dict__.keys():
                if modifier.adverb == old_word:
                    new_modifier = phrase_spec.ADV(get_rhyme_word(old_word, candidates, 'AVP'))
                    modifier_index = phrase.modifiers.index(modifier)
                    phrase.modifiers[modifier_index] = new_modifier

        new_phrases.append(phrase)

    if not new_phrases:
        new_phrases = phrases

    return new_phrases


def get_rhyme_word(old_word, candidates, pos):
    #Find the candidates in the lexicon
    lemmas = [lemma(candidate['word']) for candidate in candidates]
    filtered_lemmas = filter_candidates(lemmas, pos)
    options = [candidate for candidate in candidates if lemma(candidate['word']) in filtered_lemmas]

    if not options:
        options = candidates

    best_options = [candidate for candidate in candidates if candidate['score'] == options[0]['score']]

    return most_similar(old_word, best_options, pos)['word']


#Find the most conceptually similar words from a list of candidates
def most_similar(word, candidates, pos):
    word_synset = get_synset(word, pos)
    if word_synset is None:
        return random.choice(candidates)
    max_similarity_score = 0
    max_similarity_candidate = ''
    for candidate in candidates:
        candidate_synset = get_synset(candidate['word'], pos)
        if candidate_synset is None:
            continue
        similarity = wordnet.similarity(word_synset, candidate_synset)
        if similarity > max_similarity_score:
            max_similarity_score = similarity
            max_similarity_candidate = candidate

    if max_similarity_candidate:
        return max_similarity_candidate
    else:
        return random.choice(candidates)


def get_synset(word, pos=''):
    wpos = wordnet.NOUN
    if pos.startswith('V'):
        wpos = wordnet.VERB
    elif pos.startswith('AVP'):
        wpos = wordnet.ADVERB
    elif pos.startswith('A'):
        wpos = wordnet.ADJECTIVE

    synset = None
    try:
        if pos:
            synset = wordnet.synsets(singularize(lemmatise(word)), wpos)[0]
        else:
            synset = wordnet.synsets(singularize(lemmatise(word)))[0]
    except IndexError:
        try:
            if pos:
                synset = wordnet.synsets(lemmatise(word), wpos)[0]
            else:
                synset = wordnet.synsets(lemmatise(word))[0]
        except IndexError:
            try:
                if pos:
                    synset = wordnet.synsets(singularize(word), wpos)[0]
                else:
                    synset = wordnet.synsets(singularize(word))[0]
            except IndexError:
                try:
                    if pos:
                        synset = wordnet.synsets(word, wpos)[0]
                    else:
                        synset = wordnet.synsets(word)[0]
                except IndexError:
                    pass

    if pos:
        return get_synset(word)

    return synset


def get_property(target_word, pos, used):
    options = [tail for head, tail, relation in builder.knowledge if
               relation == 'HasProperty' and head == target_word and tail not in used]
    if options:
        return random.choice(options)

    if pos.startswith('v'):
        wpos = wordnet.VERB
    else:
        wpos = wordnet.NOUN
    synonyms = builder.get_synonyms(target_word, wpos)
    for synonym in synonyms:
        options = [tail for head, tail, relation in builder.knowledge if
                   relation == 'HasProperty' and head == synonym and tail not in used]
        if options:
            return random.choice(options)

    if pos.startswith('v'):
        return get_random_word('AVP')

    return get_random_word('A')