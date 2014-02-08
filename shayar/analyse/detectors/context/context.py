__author__ = 'Nitin'

from pattern.text.en import parsetree
from nltk.corpus import verbnet
from urllib2 import urlopen
from shayar.character import Character
from json import loads as json_load
from semantic_dependency_node import SemanticDependencyNode
from character_builder import create_characters
from frame_to_relation_converter import build_candidate_relations_from_frames

NEXT_CHARACTER_ID = 0

def build_story(poem):
    lines = ""
    for line in poem:
        lines += line.lower() + " "

    parse_sentences = parsetree(lines, tags=True, chunks=True, relations=True, lemmata=True, tagset=True)

    sentences = [sentence.string for sentence in parse_sentences]

    for sentence in sentences:
        json_parse_data = make_request(sentence)
        dependencies = get_dependencies(json_parse_data)
        characters = create_characters([d for d in dependencies if d['CHARACTER_ID']])
        candidate_relations = build_candidate_relations_from_frames(json_parse_data, dependencies)
        print candidate_relations
        #Find the root.
        root = [dep for dep in dependencies if dep['HEAD'] == '0'][0]
        root_node = build_semantic_dependency_tree(dependencies, root, characters)


def build_semantic_dependency_tree(dependencies, root, characters):
    root_node = SemanticDependencyNode(root['ID'], root['FORM'], root['CPOSTAG'], root['POSTAG'])

    if root['CHARACTER_ID']:
        root_node.add_character(characters[root['ID']])

    children = [dep for dep in dependencies if dep['HEAD'] == root['ID']]
    for child in children:
        child_node = build_semantic_dependency_tree(dependencies, child, characters)
        root_node.add_child(child['DEPREL'], child_node)

    return root_node


def get_dependencies(json):
    full = json["sentences"][0]["conll"]
    entries = full.split('\n')
    dependencies = []
    for entry in entries:
        dependency = {}
        entry = entry.split('\t')
        dependency['ID'] = entry[0]
        dependency['FORM'] = entry[1]
        #dependency['LEMMA'] = entry[2] but we don't get this
        dependency['CPOSTAG'] = entry[3]
        dependency['POSTAG'] = entry[4]
        #dependency['FEATS'] = entry[5] nor do we get this
        dependency['HEAD'] = entry[6]
        dependency['DEPREL'] = entry[7]
        #dependency['PHEAD'] = entry[8] nor these
        #dependency['PDEPREL'] = entry[9]
        cpostag = dependency['CPOSTAG']
        if cpostag.startswith('N') or cpostag.startswith('PR'):
            global NEXT_CHARACTER_ID
            dependency['CHARACTER_ID'] = str(NEXT_CHARACTER_ID)
            NEXT_CHARACTER_ID += 1
        else:
            dependency['CHARACTER_ID'] = ''

        dependencies.append(dependency)

    return dependencies


def make_request(sentence):
    url = "http://demo.ark.cs.cmu.edu/parse/api/v1/parse?sentence="
    request_url = url + sentence.replace(' ', '+')
    socket = urlopen(request_url)
    json = json_load(socket.read())
    socket.close()
    return json