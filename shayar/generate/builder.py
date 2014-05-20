__author__ = 'Nitin'
import xml.etree.ElementTree as ET
from framenet_reader import lu_from_frames, valence_pattern_from_id, lu_from_word, lu_from_id, get_random_word
import random

import jpype

jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=simplenlg-v4.4.2.jar")

features = jpype.JPackage('simplenlg.features')
phrasespec = jpype.JPackage('simplenlg.phrasespec')
framework = jpype.JPackage('simplenlg.framework')
lexicon = jpype.JClass('simplenlg.lexicon.Lexicon')
feature = jpype.JClass('simplenlg.features.Feature')
tense = jpype.JClass('simplenlg.features.Tense')

Realiser = jpype.JClass('simplenlg.realiser.english.Realiser')
lex = lexicon.getDefaultLexicon()
phraseFactory = framework.NLGFactory(lex)
realiser = Realiser(lex)


def build_poem_line(new_poem, template, poems, line):
    # Check for a relation in order as given in google doc

    # Use all the separate functions that will be written below to:
    # - Retrieve relevant frames from framenet
    # - Fill in the gaps in the frames

    # Do any other re-fitting (e.g. to match rhythm)

    # Add the returned phrase to the CyberPoem at this line

    #builders = [build_name_phrase, build_action_phrase, build_location_phrase, build_has_phrase, build_message_phrase, build_desire_phrase]

    #for line_index in range(0, new_poem.lines[0]):
    #    random.choice(builders)()

    build_capable_phrase()
    build_partof_phrase()
    shutdown_builder()


def build_is_phrase():
    pass


def build_hasproperty_phrase():
    pass


def build_action_phrase():
    verb = str(get_random_word('V'))
    try:
        lu = lu_from_word(verb, 'v')
    except IndexError:
        raise Exception('Given word is not a verb, look for synonyms: ' + verb)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print_nlg_statement(valence_pattern, lu)


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
                new_elem = phraseFactory.createNounPhrase(get_random_word(pos))
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('V'):
                new_elem = phraseFactory.createVerbPhrase(get_random_word(pos))
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('P'):
                new_elem = phraseFactory.createPrepositionPhrase(pos.partition('[')[-1].rpartition(']')[0])
                n = phraseFactory.createNounPhrase(get_random_word(pos))
                new_elem.addComplement(n)
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

        if not starters_done:
            word = lu.get('name').rpartition('.')[0]
            pos = lu.get('name').partition('.')[-1].upper()
            if pos.startswith('N'):
                new_elem = phraseFactory.createNounPhrase(word)
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('V') or pos.startswith('A'):
                new_elem = phraseFactory.createVerbPhrase(word)
                new_elem.setFeature(feature.TENSE, tense.PAST)
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('P'):
                new_elem = phraseFactory.createPrepositionPhrase(pos.partition('[')[-1].rpartition(']')[0])
                n = phraseFactory.createNounPhrase(word)
                new_elem.addComplement(n)
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            starters_done = True

        phrases.append(group_phrase_elem)

    phrases = phrases[:2] + [phraseFactory.createNounPhrase(name)] + phrases[2:]

    if len(phrases) > 2:
        line = phraseFactory.createClause(phrases[0], phrases[1], phrases[2])
    elif len(phrases) > 1:
        line = phraseFactory.createClause(phrases[0], phrases[1])
    else:
        line = phrases[0]

    print realiser.realise(line).getRealisation()


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


def shutdown_builder():
    jpype.shutdownJVM()


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
        group_phrase_elem = None
        for valence_unit in group:

            pos = valence_unit.get('PT')
            if pos.startswith('N'):
                new_elem = phraseFactory.createNounPhrase(get_random_word(pos))
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('V'):
                new_elem = phraseFactory.createVerbPhrase(get_random_word(pos))
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('P'):
                new_elem = phraseFactory.createPrepositionPhrase(pos.partition('[')[-1].rpartition(']')[0])
                n = phraseFactory.createNounPhrase(get_random_word(pos))
                new_elem.addComplement(n)
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

        if not starters_done:
            word = lu.get('name').rpartition('.')[0]
            pos = lu.get('name').partition('.')[-1].upper()
            if pos.startswith('N'):
                new_elem = phraseFactory.createNounPhrase(word)
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('V'):
                new_elem = phraseFactory.createVerbPhrase(word)
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            elif pos.startswith('P'):
                new_elem = phraseFactory.createPrepositionPhrase(pos.partition('[')[-1].rpartition(']')[0])
                n = phraseFactory.createNounPhrase(word)
                new_elem.addComplement(n)
                if group_phrase_elem:
                    group_phrase_elem.addComplement(new_elem)
                else:
                    group_phrase_elem = new_elem

            starters_done = True

        phrases.append(group_phrase_elem)

    if len(phrases) > 2:
        line = phraseFactory.createClause(phrases[0], phrases[1], phrases[2])
    elif len(phrases) > 1:
        line = phraseFactory.createClause(phrases[0], phrases[1])
    else:
        line = phrases[0]

    print realiser.realise(line).getRealisation()