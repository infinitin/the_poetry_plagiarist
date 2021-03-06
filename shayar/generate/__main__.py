__author__ = 'Nitin'
# This import is required for the pickle load
# noinspection PyUnresolvedReferences,PyPep8Naming
from shayar.poem_template import Template
import os
import cPickle
import json
from initialisation import init_poem
from cyber_poem import CyberPoem
from shayar.generalise.utils import retrieve_all_poems
import utils
from creation import create_poem
from creation import shutdown_builder
from shayar.knowledge.knowledge import retrieve_knowledge

import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__)


#Grab the poem template of a particular collection from store
def retrieve_template(coll):
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\generalise', coll + '.template')), 'rb')
    stored_template = cPickle.load(f)
    f.close()
    return stored_template

#Input from user
logging.info('Getting user input')
json_input = '{"collection": "limericks"}'
settings = json.loads(json_input)
collection = settings["collection"]

#Get template, poems from store
logging.info('Getting template and poems from store')
template = retrieve_template(collection)
poems = retrieve_all_poems(collection)
utils.num_poems = len(poems)

#Init poem
logging.info('Initialising poem')
new_poem = CyberPoem()
init_poem(new_poem, template)

#Build all the lines. May want to do first line, then some aggregation, then subsequent lines later on
logging.info('Creating poem')
retrieve_knowledge()
create_poem(new_poem, template)

#Realise poem into the CyberPoem.poem attribute and return to user
logging.info('Realising poem')
new_poem.realise()

shutdown_builder()