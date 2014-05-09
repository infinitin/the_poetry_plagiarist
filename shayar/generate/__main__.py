__author__ = 'Nitin'
# This import is required for the pickle load
# noinspection PyUnresolvedReferences,PyPep8Naming
from shayar.poem_template import Template
import os
import cPickle
import json
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)

from initialisation import init_poem


#Grab the poem template of a particular collection from store
#def retrieve_template(collection):
#    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\generalise', collection + '.template')), 'rb')
#    poems = cPickle.load(f)
#    f.close()
#    return poems


#json_input = '{"collection": "limericks", "plot": true, "persist": false}'
#settings = json.loads(json_input)

#template = retrieve_template(settings["collection"])

#new_poem = init_poem(settings)
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

man = phraseFactory.createNounPhrase('the', 'man')
man.addPostModifier('angry')
man.addPreModifier('so')

output = realiser.realise(man).getRealisation()
print output

jpype.shutdownJVM()

