__author__ = 'Nitin'

from pattern.text.en import parsetree
from urllib2 import urlopen
from json import loads as json_load
from semantic_dependency_node import SemanticDependencyNode
from character_builder import create_characters
from frame_to_relation_converter import build_candidate_relations_from_frames
from concept_relation_builder import build_relations


def build_story(poem):
    lines = ""
    for line in poem:
        lines += line.lower() + " "

    parse_sentences = parsetree(lines, tags=True, chunks=True, relations=True, lemmata=True, tagset=True)

    sentences = [sentence.string for sentence in parse_sentences]

    for sentence in sentences:
        json_parse_data = make_request(sentence)
        dependencies = get_dependencies(json_parse_data)
        characters = create_characters(dependencies, json_parse_data["sentences"][0]["frames"])
        candidate_relations = build_candidate_relations_from_frames(json_parse_data, dependencies)
        print candidate_relations
        #Find the root.
        root = [dep for dep in dependencies if dep['HEAD'] == '0'][0]
        root_node = build_semantic_dependency_tree(dependencies, root, characters, candidate_relations)
        build_relations(root_node)


def build_semantic_dependency_tree(dependencies, root, characters, candidate_relations):
    root_node = SemanticDependencyNode(root['ID'], root['FORM'], root['CPOSTAG'], root['POSTAG'])

    if root['CHARACTER_ID']:
        root_node.add_character(characters[root['ID']])

    try:
        root_node.add_candidate_relation(candidate_relations[root['FORM']])
    except KeyError:
        pass

    children = [dep for dep in dependencies if dep['HEAD'] == root['ID']]
    for child in children:
        child_node = build_semantic_dependency_tree(dependencies, child, characters, candidate_relations)
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
        dependencies.append(dependency)

    return dependencies


def make_request(sentence):
    url = "http://demo.ark.cs.cmu.edu/parse/api/v1/parse?sentence="
    request_url = url + sentence.replace(' ', '+')
    socket = urlopen(request_url)
    json = json_load(socket.read())
    socket.close()
    return json