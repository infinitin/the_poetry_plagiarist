__author__ = 'Nitin'
from framenet_reader import lu_from_frames, valence_pattern_from_id, lu_from_word, lu_from_id, get_random_word
import random
import phrase_spec
from rephrase import fit_rhythm_pattern, fit_rhyme
from pattern.text.en import wordnet, VERB
import logging
import creation


def build_is_phrase():
    pass


def build_hasproperty_phrase():
    pass


def build_action_phrase(verb, pattern, rhyme_token):
    verb = str(get_random_word('V'))

    alternatives = []
    tried_alternatives = set()
    synset = wordnet.synsets(verb, pos=VERB)
    if synset:
        alternatives = synset[0].synonyms

    valence_pattern = []
    lu = None
    while not valence_pattern:
        tried_alternatives.add(verb)
        lu = None
        while lu is None:
            try:
                lu = lu_from_word(verb, 'v')
            except IndexError:
                logging.info("I don't know how to use this word, looking for alternatives: " + verb)
                tried_alternatives.add(verb)
                remaining_alternatives = [word for word in alternatives if word not in tried_alternatives]
                if remaining_alternatives:
                    verb = random.choice(remaining_alternatives)
                else:
                    verb = get_random_word('V')

        valence_pattern = valence_pattern_from_id(lu.get('ID'))

    phrases = create_phrases(valence_pattern, lu)

    phrases = fit_rhythm_pattern(phrases, pattern)

    phrases = fit_rhyme(phrases, rhyme_token, pattern)

    return phrases


def build_name_phrase():
    name = 'Mary'
    frames = ['Referring_by_name']
    lu = random.choice([lu_from_frames(frames), lu_from_id('5544')])
    valence_pattern = valence_pattern_from_id(lu.get('ID'))

    phrases = []
    starters_done = False
    for group in valence_pattern:
        group_phrase_elem = None
        for valence_unit in group:

            pos = valence_unit.get('PT')
            if pos.startswith('N'):
                new_elem = creation.phraseFactory.createNounPhrase(get_random_word(pos))
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('V'):
                new_elem = creation.phraseFactory.createVerbPhrase(get_random_word(pos))
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('P'):
                new_elem = creation.phraseFactory.createPrepositionPhrase(pos.partition('[')[-1].rpartition(']')[0])
                n = creation.phraseFactory.createNounPhrase(get_random_word(pos))
                new_elem.addComplement(n)
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

        if not starters_done:
            word = lu.get('name').rpartition('.')[0]
            pos = lu.get('name').partition('.')[-1].upper()
            if pos.startswith('N'):
                new_elem = creation.phraseFactory.createNounPhrase(word)
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('V') or pos.startswith('A'):
                new_elem = creation.phraseFactory.createVerbPhrase(word)
                new_elem.setFeature(creation.feature.TENSE, creation.tense.PAST)
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('P'):
                new_elem = creation.phraseFactory.createPrepositionPhrase(pos.partition('[')[-1].rpartition(']')[0])
                n = creation.phraseFactory.createNounPhrase(word)
                new_elem.addComplement(n)
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            starters_done = True

        phrases.append(group_phrase_elem)

    phrases = phrases[:2] + [creation.phraseFactory.createNounPhrase(name)] + phrases[2:]
    phrases[0].setDeterminer('a')  # FIXME: 'an' if starts with vowel phoneme

    if len(phrases) > 2:
        line = creation.phraseFactory.createClause(phrases[0], phrases[1], phrases[2])
    elif len(phrases) > 1:
        line = creation.phraseFactory.createClause(phrases[0], phrases[1])
    else:
        line = phrases[0]

    print creation.realiser.realise(line).getRealisation()


#FIXME: Guarantee a location for the object
def build_location_phrase():
    frames = ['Being_located']
    lu = random.choice([lu_from_frames(frames), lu_from_id('10640')])
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print_nlg_statement(valence_pattern, lu)


#FIXME: Make sure that you check the pos of the 'has' word - sometimes noun, sometimes verb
def build_has_phrase():
    # Need to use possessive pronouns as well
    frames = ['Possession']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print_nlg_statement(valence_pattern, lu)


def build_message_phrase():
    frames = ['Communication', 'Telling', 'Statement', 'Chatting']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print_nlg_statement(valence_pattern, lu)


def build_desire_phrase():
    frames = ['Desiring']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print_nlg_statement(valence_pattern, lu)


#FIXME: This is pretty bad
def build_capable_phrase():
    frames = ['Capability']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print_nlg_statement(valence_pattern, lu)


#FIXME: This is pretty bad too
def build_partof_phrase():
    frames = ['Part_inner_outer', 'Part_ordered_segments', 'Part_piece', 'Part_whole', 'Inclusion']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print_nlg_statement(valence_pattern, lu)


def print_frame(lu, valence_pattern):
    printed = False
    for group in valence_pattern:
        for valence_unit in group:
            print valence_unit.get('GF') + ', ' + valence_unit.get('PT') + ', ' + valence_unit.get('FE')
        if not printed:
            print str(lu.get('name'))
            printed = True
    print ''


def print_filled_gaps(valence_pattern, lu):
    words = []
    starters_done = False
    for group in valence_pattern:
        for valence_unit in group:
            pos = valence_unit.get('PT')
            if pos.startswith('P'):
                words.append(pos.partition('[')[-1].rpartition(']')[0])
            words.append(get_random_word(pos))
        if not starters_done:
            words.append(lu.get('name'))
            starters_done = True

    print ' '.join(words)


def print_nlg_statement(valence_pattern, lu):
    phrases = []
    starters_done = False
    for group in valence_pattern:
        group_phrase_elem = ()
        for valence_unit in group:

            pos = valence_unit.get('PT')
            if pos.startswith('N'):
                new_elem = creation.phraseFactory.createNounPhrase(get_random_word(pos))
                if group_phrase_elem:
                    group_phrase_elem[0].addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('V'):
                new_elem = creation.phraseFactory.createVerbPhrase(get_random_word(pos))
                if group_phrase_elem:
                    group_phrase_elem[0].addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('P'):
                new_elem = creation.phraseFactory.createPrepositionPhrase(pos.partition('[')[-1].rpartition(']')[0])
                n = creation.phraseFactory.createNounPhrase(get_random_word(pos))
                new_elem.addComplement(n)
                if group_phrase_elem:
                    group_phrase_elem[0].addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

        if not starters_done:
            word = lu.get('name').rpartition('.')[0]
            pos = lu.get('name').partition('.')[-1].upper()
            if pos.startswith('N'):
                new_elem = creation.phraseFactory.createNounPhrase(word)
                if group_phrase_elem:
                    group_phrase_elem[0].addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('V'):
                new_elem = creation.phraseFactory.createVerbPhrase(word)
                if group_phrase_elem:
                    group_phrase_elem[0].addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('P'):
                new_elem = creation.phraseFactory.createPrepositionPhrase(pos.partition('[')[-1].rpartition(']')[0])
                n = creation.phraseFactory.createNounPhrase(word)
                new_elem.addComplement(n)
                if group_phrase_elem:
                    group_phrase_elem[0].addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            starters_done = True

        phrases.append(group_phrase_elem)

    print creation.realise(make_clause(phrases)).getRealisation()


def create_phrases(valence_pattern, lu):
    phrases = []
    starters_done = False
    for group in valence_pattern:
        phrase = None
        for valence_unit in group:

            pos = valence_unit.get('PT')
            if pos.startswith('N'):
                new_elem = phrase_spec.NP(get_random_word(pos))
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            elif pos.startswith('V'):
                new_elem = phrase_spec.VP(get_random_word(pos))
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            elif pos.startswith('P'):
                n = phrase_spec.NP(get_random_word(pos))
                new_elem = phrase_spec.PP(pos.partition('[')[-1].rpartition(']')[0], n)
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

        if not starters_done:
            phrases.append(phrase)
            phrase = None
            word = lu.get('name').rpartition('.')[0]
            pos = lu.get('name').partition('.')[-1].upper()
            if pos.startswith('N'):
                new_elem = phrase_spec.NP(word)
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            elif pos.startswith('V'):
                new_elem = phrase_spec.VP(word)
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            elif pos.startswith('P'):
                n = phrase_spec.NP(word)
                new_elem = phrase_spec.PP(pos.partition('[')[-1].rpartition(']')[0], n)
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            starters_done = True

        phrases.append(phrase)

    return [phrase for phrase in phrases if phrase is not None]


def make_clause(spec_phrases):
    phrases = []

    for spec_phrase in spec_phrases:
        phrases.append(spec_phrase.translate_to_nlg())

    if len(phrases) > 2:
        line = creation.phraseFactory.createClause(phrases[0], phrases[1], phrases[2])
        for phrase in phrases[3:]:
            line.addComplement(phrase)
    elif len(phrases) > 1:
        line = creation.phraseFactory.createClause(phrases[0], phrases[1])
    else:
        line = phrases[0]

    return line