__author__ = 'Nitin'

import logging
from pattern.text.en import parsetree
from urllib2 import urlopen, URLError
from json import loads as json_load
from character_builder import create_characters
from frame_to_relation_converter import build_candidate_relations_from_frames
from anaphora_resolution import resolve_anaphora
from shayar.analyse.detectors.utils import replace_contractions
from relation_builder import build_relations, remove_location_preps
from personification import determine_personification


def identify_characters_and_relationships(poem):
    # Break it down into lines and lower all characters.
    # NOTE: This may cause some issues with pronouns and I
    lines = ""
    for line in poem:
        line = replace_contractions(line)
        lines += line.lower() + " "

    # Split into natural sentences.
    parse_sentences = parsetree(lines, tags=True, chunks=True, relations=True, lemmata=True, tagset=True)
    sentences = [sentence.string for sentence in parse_sentences]

    all_characters = []

    # Send a sentence at a time to Noah's Ark.
    # Simplify the dependency tree by chunking based on certain dependencies.
    # Create the character objects out of these dependencies.
    # Determine relations from the Semafor Frame-Semantic parse.
    # Build relations for each character based on the relations from Semafor and the dependencies.
    # Remove location prepositions from characters texts and is_a relations
    # Save all the characters for anaphora resolution later and to be returned for abstraction.
    for sentence in sentences:
        json_parse_data = make_request(sentence)
        dependencies = collapse_loose_leaves(get_dependencies(json_parse_data))
        characters = create_characters(dependencies)
        candidate_relations = build_candidate_relations_from_frames(json_parse_data["sentences"][0]["frames"])
        build_relations(dependencies, characters, candidate_relations)
        remove_location_preps(characters)
        determine_personification(characters, json_parse_data["sentences"][0]["frames"], dependencies)
        all_characters.extend(characters)

    # Perform anaphora resolution of all types.
    resolve_anaphora(all_characters)

    return all_characters


# We want to deal with characters, actions and descriptions on a phrase by phrase level. This increases accuracy and
#  simplifies the problem as well. We chunk phrases together by collapsing branches of the type below. See doc for
#  explanation on each of them.
# Note that by default we keep the POS of the highest dep, but in some cases we must inherit the POS
#  e.g. tasted so nice should inherit the adjective POS from nice rather than keeping the verb POS of tasted.
def collapse_loose_leaves(dependencies):
    collapsable_branches = ['acomp', 'advmod', 'aux', 'cop', 'dep', 'det', 'measure', 'nn', 'num', 'number', 'neg', 'preconj',
                            'predet', 'prep', 'pobj', 'quantmod']

    non_leaves_nums = set([dependency['HEAD'] for dependency in dependencies])
    leaves = [dependency for dependency in dependencies if dependency['ID'] not in non_leaves_nums]
    leaves.reverse()

    for leaf in leaves:
        curr_leaf = leaf
        deprel = curr_leaf['DEPREL']
        while deprel in collapsable_branches:
            if deprel == 'prep' and not curr_leaf['FORM'].startswith('of'):
                break

            #Get the parent (long way so that we can change dependencies directly by reference)
            for dep in dependencies:
                if dep['ID'] == curr_leaf['HEAD']:
                    parent = dep
                    break

            #Pass the form on to the parent to append unless it is a cop dependency
            if not deprel == 'cop':
                if int(parent['ID']) < int(curr_leaf['ID']):
                    parent['FORM'] += ' ' + curr_leaf['FORM']
                else:
                    parent['FORM'] = curr_leaf['FORM'] + ' ' + parent['FORM']

            #Preserve this postag by changing the parent's
            if (curr_leaf['POSTAG'].startswith('J') and parent['POSTAG'].startswith('V') and deprel == 'dep') or \
                            deprel == 'pobj' or deprel == 'acomp' or deprel == 'prep':
                parent['CPOSTAG'] = curr_leaf['CPOSTAG']
                parent['POSTAG'] = curr_leaf['POSTAG']

            #delete this from dependencies
            dependencies.remove(curr_leaf)
            #change deprel to the parent deprel
            deprel = parent['DEPREL']
            curr_leaf = parent

    return dependencies


# Extract the dependencies from the Syntactic Dependency Parse from TurboParser CoNLL API call
def get_dependencies(json):
    full = json["sentences"][0]["conll"]
    entries = full.split('\n')
    dependencies = []
    for entry in entries:
        dependency = {}
        entry = entry.split('\t')
        dependency['ID'] = entry[0]
        dependency['FORM'] = entry[1]
        dependency['CPOSTAG'] = entry[3]
        dependency['POSTAG'] = entry[4]
        dependency['HEAD'] = entry[6]
        dependency['DEPREL'] = entry[7]
        dependencies.append(dependency)

    return dependencies


#Make an API request to Noah's Ark to get the Syntactic Dependency and Frame-Semantic Parses in JSON form
def make_request(sentence):
    url = "http://demo.ark.cs.cmu.edu/parse/api/v1/parse?sentence="
    request_url = url + sentence.replace(' ', '+')
    try:
        socket = urlopen(request_url)
        json = json_load(socket.read())
        socket.close()
    except URLError:
        logging.error("You are not connected to the Internet!")
    return json