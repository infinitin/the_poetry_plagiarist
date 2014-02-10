__author__ = 'Nitin'

from pattern.text.en import parsetree
from urllib2 import urlopen
from json import loads as json_load
from semantic_dependency_node import SemanticDependencyNode
from character_builder import create_characters
from frame_to_relation_converter import build_candidate_relations_from_frames
from anaphora_resolution import resolve_anaphora

negative_words = set(['not', 'seldom', 'hardly', 'barely', 'scarcely', 'rarely', 'no', 'neither', "n't"])


def build_story(poem):
    lines = ""
    for line in poem:
        lines += line.lower() + " "

    parse_sentences = parsetree(lines, tags=True, chunks=True, relations=True, lemmata=True, tagset=True)

    sentences = [sentence.string for sentence in parse_sentences]

    all_characters = []

    for sentence in sentences:
        json_parse_data = make_request(sentence)
        dependencies = collapse_loose_leaves(get_dependencies(json_parse_data))
        characters = create_characters(dependencies)
        candidate_relations = build_candidate_relations_from_frames(json_parse_data, dependencies, characters)
        #We probably won't need this stuffFind the root.
        #root = [dep for dep in dependencies if dep['HEAD'] == '0'][0]
        #root_node = build_semantic_dependency_tree(dependencies, root, characters, candidate_relations)
        build_relations(dependencies, characters, candidate_relations)
        all_characters.extend(characters)

    resolve_anaphora(all_characters)
    for character in all_characters:
        print character


def build_relations(dependencies, characters, candidate_relations):
    for character in characters:
        for dependency in dependencies:
            if character.character_id == dependency['ID']:
                related_dependencies = get_all_related_dependencies(dependency, dependencies, candidate_relations)
                for related_dependency in related_dependencies:
                    determine_relation_types(related_dependency, character)

    # Make this less hacky pls.
    n = 1
    for character in characters:
        first_has_property = character.has_property
        first_not_has_property = character.not_has_property
        for i in range(n, len(characters)):
            second_has_property = characters[n].has_property
            second_not_has_property = characters[n].not_has_property
            for has_p in second_has_property:
                if has_p in first_has_property:
                    first_has_property.remove(has_p)
            for not_has_p in second_not_has_property:
                if not_has_p in first_not_has_property:
                    first_not_has_property.remove(not_has_p)
            n += 1


def determine_relation_types(related_dependency, character):
    deprel = related_dependency[0]
    form = related_dependency[1]['FORM']

    if deprel == 'amod' or deprel == 'conj' or deprel == 'poss' or related_dependency[1]['POSTAG'].startswith('J'):
        relation = 'HasProperty'
        negatives = [neg for neg in set(form.split(' ')) if neg in negative_words]
        if len(negatives) % 2 == 1:
            relation = 'Not' + relation
            words = form.split(' ')
            form = ' '.join(words[words.index(negatives[-1])+1:])

        character.add_relation(relation, form)

    elif deprel == 'cop':
        pass
        #character.add_relation('IsA', form)

    elif deprel == 'nsubjpass' or deprel == 'dobj':
        character.add_relation('ReceivesAction', form)
        
    elif deprel == 'prep':
        pass
        #character.add_relation('AtLocation', form)
        
    elif deprel == 'xsubj' or deprel == 'rcmod':
        character.add_relation('CapableOf', form)

    elif related_dependency[1]['POSTAG'].startswith('V'):
        character.add_relation('TakesAction', form)


def get_all_related_dependencies(dependency, dependencies, candidate_relations):
    related_dependencies = []

    in_deps = get_in_dependencies(dependency, dependencies, candidate_relations)

    for in_dep in in_deps:
        related_dependencies.append(in_dep)

    out_deps = get_out_dependencies(dependency, dependencies, candidate_relations)

    for out_dep in out_deps:
        related_dependencies.append(out_dep)

    return related_dependencies


def get_out_dependencies(dependency, dependencies, candidate_relations):
    out_deps = []
    for dep in dependencies:
        #Ignore subtree if it has a candidate relation (for now) since they are already added
        try:
            candiate_relation = candidate_relations[dep['FORM']]
            continue
        except KeyError:
            if dep['HEAD'] == dependency['ID']:
                    out_dep = dep['DEPREL'], dep
                    out_deps.append(out_dep)
                    out_deps.extend(get_out_dependencies(dep, dependencies, candidate_relations))

    return out_deps


def get_in_dependencies(dependency, dependencies, candidate_relations):
    in_deps = []
    for dep in dependencies:
        #Ignore subtree if it has a candidate relation (for now) since they are already added
        try:
            candiate_relation = candidate_relations[dep['FORM']]
            continue
        except KeyError:
            if dep['ID'] == dependency['HEAD']:
                in_dep = dependency['DEPREL'], dep
                in_deps.append(in_dep)
                dependencies_without_this_one = dependencies
                dependencies_without_this_one.remove(dependency)
                in_deps.extend(get_out_dependencies(dep, dependencies_without_this_one, candidate_relations))

    return in_deps


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


def collapse_loose_leaves(dependencies):
    collapsable_branches = ['acomp', 'advmod', 'dep', 'det', 'measure', 'nn', 'num', 'number', 'neg', 'preconj',
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

            #Pass the form on to the parent to append
            if (int(parent['ID']) < int(curr_leaf['ID'])):
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