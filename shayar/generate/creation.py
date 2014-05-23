__author__ = 'Nitin'
from builder import build_action_phrase

import jpype

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
    for letter in template.rhyme_schemes[0]:
        rhyme_scheme[letter] = []
    #Send to builder
    for l in range(0, sum(new_poem.lines)):
        # Check for a relation in order as given in google doc

        # Use all the separate functions that will be written below to:
        # - Retrieve relevant frames from framenet
        # - Fill in the gaps in the frames

        # Do any other re-fitting (e.g. to match rhythm)

        # Add the returned phrase to the CyberPoem at this line

        #builders = [build_name_phrase, build_action_phrase, build_location_phrase, build_has_phrase, build_message_phrase,
        #            build_desire_phrase]
        #random.choice(builders)(pattern)

        phrases = build_action_phrase('', template.stress_patterns[l], template.rhyme_schemes[0][l])

        new_poem.phrases.append(phrases)

    #TODO: Don't forget the persona creation module
    #TODO: Also gotta make distinct sentences without losing stress patterns


def shutdown_builder():
    jpype.shutdownJVM()