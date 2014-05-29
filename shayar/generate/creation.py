__author__ = 'Nitin'
from builder import *
import logging
import jpype
import builder
from shayar.character import Character

jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=simplenlg-v4.4.2.jar")

framework = jpype.JPackage('simplenlg.framework')
lexicon = jpype.JClass('simplenlg.lexicon.Lexicon')
Realiser = jpype.JClass('simplenlg.realiser.english.Realiser')
lex = lexicon.getDefaultLexicon()
phraseFactory = framework.NLGFactory(lex)
realiser = Realiser(lex)

features = jpype.JPackage('simplenlg.features')
phrasespec = jpype.JPackage('simplenlg.phrasespec')
feature = jpype.JClass('simplenlg.features.Feature')
lexical_feature = jpype.JClass('simplenlg.features.LexicalFeature')
gender = jpype.JClass('simplenlg.features.Gender')
number_agreement = jpype.JClass('simplenlg.features.NumberAgreement')
tense = jpype.JClass('simplenlg.features.Tense')
person = jpype.JClass('simplenlg.features.Person')
internal_feature = jpype.JClass('simplenlg.features.InternalFeature')
lexical_category = jpype.JClass('simplenlg.framework.LexicalCategory')

rhyme_scheme = {}


def create_poem(new_poem, template):
    logging.info('Setting up rhyme scheme map')
    for letter in template.rhyme_schemes[0]:
        rhyme_scheme[letter] = []

    #FIXME: REMOVE BELOW LATER
    test_character = Character(0, 'sg', 'n', 'a')
    test_character.add_relation('IsA', 'pony')
    test_character.add_relation('Desires', 'run')
    builder.characters = [test_character]
    #FIXME: REMOVE ABOVE LATER

    #builder.characters = new_poem.characters
    #Send to builder
    for l in range(0, sum(new_poem.lines)):
        logging.info('Building line ' + str(l))
        #Set globals
        builder.pattern = template.stress_patterns[l]
        builder.rhyme_token = template.rhyme_schemes[0][l]

        # Check for a relation in order as given in google doc
        #  Need to make sure that we don't pick the same relation twice
        builder.character_i = builder.characters.index(random.choice(builder.characters))
        builder.dep_pronominal = False
        builder.obj_pronominal = False
        builder.subj_pronominal = False
        #relation = random.choice(flatten(builder.characters[builder.character_index].relations.values()))

        # Use all the separate builder funtions to build phrases (lines of poetry)
        #phrases = build_name_phrase('Mary')
        phrases = build_location_phrase('Japan')
        #phrases = build_hasproperty_phrase('happy')
        #desire = random.choice(builder.characters[builder.character_index].type_to_list['Desires'])
        #phrases = build_desire_phrase(desire)
        #phrases = build_takes_action_phrase(str(get_random_word('V')))
        #phrases = build_receives_action_phrase(str(get_random_word('V')))

        new_poem.phrases.append(phrases)

    #TODO: Don't forget the persona creation module
    #TODO: Also gotta make distinct sentences without losing stress patterns


def shutdown_builder():
    jpype.shutdownJVM()