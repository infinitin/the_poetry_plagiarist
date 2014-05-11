__author__ = 'Nitin'
# This import is required for the pickle load
# noinspection PyUnresolvedReferences,PyPep8Naming
from shayar.poem_template import Template
import os
import cPickle
import json
import jpype
from initialisation import init_poem
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)


#Grab the poem template of a particular collection from store
def retrieve_template(collection):
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\generalise', collection + '.template')), 'rb')
    stored_template = cPickle.load(f)
    f.close()
    return stored_template


json_input = '{"collection": "limericks"}'
settings = json.loads(json_input)
template = retrieve_template(settings["collection"])
new_poem = init_poem(template)

for attr in new_poem.__dict__:
    print str(attr) + ": " + str(getattr(new_poem, attr))

"""
jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=simplenlg-v4.4.2.jar")

features = jpype.JPackage('simplenlg.features')
phrasespec = jpype.JPackage('simplenlg.phrasespec')
framework = jpype.JPackage('simplenlg.framework')
lexicon = jpype.JClass('simplenlg.lexicon.Lexicon')

Realiser = jpype.JClass('simplenlg.realiser.english.Realiser')
lex = lexicon.getDefaultLexicon()
phraseFactory = framework.NLGFactory(lex)
realiser = Realiser(lex)

n1 = phraseFactory.createNounPhrase('the', 'shoes')

p1 = phraseFactory.createPrepositionPhrase('of')
n2 = phraseFactory.createNounPhrase('eskimo joe')
p1.addComplement(n2)

n1.addComplement(p1)

v1 = phraseFactory.createVerbPhrase('fell apart')
v1.addPreModifier('quickly')

p2 = phraseFactory.createPrepositionPhrase('as')
n3 = phraseFactory.createNounPhrase('he')
p2.addComplement(n3)

v1.addComplement(p2)

v2 = phraseFactory.createVerbPhrase('walked')

p3 = phraseFactory.createPrepositionPhrase('in')
n4 = phraseFactory.createNounPhrase('the snow')
p3.addComplement(n4)

v2.addComplement(p3)

n3.addComplement(v2)

n2.addModifier('old')

s = phraseFactory.createClause(n1, v1)

output = realiser.realise(s).getRealisation()
print output

jpype.shutdownJVM()
"""
