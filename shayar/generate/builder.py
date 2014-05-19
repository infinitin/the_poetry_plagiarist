__author__ = 'Nitin'
import xml.etree.ElementTree as ET
from framenet_reader import lu_from_frames, valence_pattern_from_id, lu_from_word, lu_from_id
import random
"""
import jpype

jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=simplenlg-v4.4.2.jar")

features = jpype.JPackage('simplenlg.features')
phrasespec = jpype.JPackage('simplenlg.phrasespec')
framework = jpype.JPackage('simplenlg.framework')
lexicon = jpype.JClass('simplenlg.lexicon.Lexicon')

Realiser = jpype.JClass('simplenlg.realiser.english.Realiser')
lex = lexicon.getDefaultLexicon()
phraseFactory = framework.NLGFactory(lex)
realiser = Realiser(lex)
"""
FRAMENET_LOC = 'C:\\Python27\\framenet_data'


def build_poem_line(new_poem, template, poems, line):
    # Check for a relation in order as given in google doc

    # Use all the separate functions that will be written below to:
    # - Retrieve relevant frames from framenet
    # - Fill in the gaps in the frames

    # Do any other re-fitting (e.g. to match rhythm)

    # Add the returned phrase to the CyberPoem at this line
    build_name_phrase()
    build_location_phrase()
    build_capable_phrase()
    build_desire_phrase()
    build_has_phrase()
    build_partof_phrase()
    build_message_phrase()
    build_action_phrase('chase')


def build_is_phrase():
    pass


def build_hasproperty_phrase():
    pass


def build_action_phrase(verb):
    try:
        lu = lu_from_word(verb, 'v')
    except IndexError:
        raise Exception('Given word is not a verb, look for synonyms.')
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print 'ACTION'
    print_frame(lu, valence_pattern)


def build_name_phrase():
    frames = ['Referring_by_name']
    lu = random.choice([lu_from_frames(frames), lu_from_id('5544')])
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print 'NAME'
    print_frame(lu, valence_pattern)


def build_location_phrase():
    frames = ['Being_located']
    lu = random.choice([lu_from_frames(frames), lu_from_id('10640')])
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print 'LOCATION'
    print_frame(lu, valence_pattern)


def build_has_phrase():
    # Need to use possessive pronouns as well
    frames = ['Possession']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print 'HAS'
    print_frame(lu, valence_pattern)


def build_message_phrase():
    frames = ['Communication', 'Telling', 'Statement', 'Chatting']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print 'MESSAGE'
    print_frame(lu, valence_pattern)


def build_desire_phrase():
    frames = ['Desiring']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print 'DESIRE'
    print_frame(lu, valence_pattern)


def build_capable_phrase():
    frames = ['Capability']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print 'CAPABLE'
    print_frame(lu, valence_pattern)


def build_partof_phrase():
    frames = ['Part_inner_outer', 'Part_ordered_segments', 'Part_piece', 'Part_whole', 'Inclusion']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print 'PARTOF'
    print_frame(lu, valence_pattern)


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