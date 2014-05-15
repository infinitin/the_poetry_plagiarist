__author__ = 'Nitin'
import xml.etree.ElementTree as ET
from framenet_reader import lu_from_frames, valence_pattern_from_id, lu_from_word
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
FRAMENET_LOC = 'C:\\Python27\\nltk_data\\corpora\\framenet_v15'


def build_poem_line(new_poem, template, poems, line):
    # Check for a relation in order as given in google doc

    # Use all the separate functions that will be written below to:
    # - Retrieve relevant frames from framenet
    # - Fill in the gaps in the frames
    # - Do any other re-fitting

    # Add the returned phrase to the CyberPoem at this line
    build_name_phrase()


def build_is_phrase():
    pass


def build_hasproperty_phrase():
    pass


def build_action_phrase():
    pass


def build_name_phrase():
    frames = ['Referring_by_name']
    lu = random.choice([lu_from_frames(frames), lu_from_word('named', 'a')])
    valence_pattern = valence_pattern_from_id(lu.get('ID'))

    print str(lu.get('name'))
    for valence_unit in valence_pattern:
        print valence_unit.get('GF') + ', ' + valence_unit.get('PT') + ', ' + valence_unit.get('FE')


def build_location_phrase():
    pass


def build_has_phrase():
    pass


def build_message_phrase():
    pass


def build_desire_phrase():
    pass


def build_capable_phrase():
    pass


def build_partof_phrase():
    pass


def shutdown_builder():
    jpype.shutdownJVM()