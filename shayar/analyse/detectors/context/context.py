__author__ = 'Nitin'

from pattern.text.en import parsetree
from urllib2 import urlopen
from json import loads as json_load
from character_builder import create_characters
from frame_to_relation_converter import build_candidate_relations_from_frames
from anaphora_resolution import resolve_anaphora
from shayar.analyse.detectors.utils import replace_contractions

# List of words that imply a negative. Used in conjunction with the 'neg' dependency
negative_words = {'not', 'seldom', 'hardly', 'barely', 'scarcely', 'rarely', 'no', 'neither', "n't"}

#All of the location prepositions (as opposed to any others)
single_at_location_preps = {'abaft', 'aboard', 'about', 'above', 'across', 'after', 'against', 'along', 'alongside',
                            'amid', 'amidst', 'among', 'amongst', 'anenst', 'around', 'aside', 'astride', 'at',
                            'athwart', 'atop', 'before', 'behind', 'below', 'beneath', 'beside', 'besides',
                            'between', 'betwixt', 'by', 'down', 'forenenst', 'in', 'inside', 'into', 'mid', 'midst',
                            'near', 'next', 'nigh', 'on', 'onto', 'opposite', 'outside', 'over', 'through', 'thru',
                            'toward', 'towards', 'under', 'underneath', 'up', 'upon', 'with', 'within', 'behither',
                            'betwixen', 'betwixt', 'biforn', 'ere', 'fornent', 'gainst', "'gainst", 'neath',
                            "'neath", 'overthwart', 'twixt', "'twixt"}

double_at_location_preps = {'ahead of', 'back to', 'close to', 'in to', 'inside of', 'left of', 'near to',
                            'next to', 'on to', 'outside of', 'right of'}

triple_at_location_preps = {'in front of', 'on top of'}

single_not_at_location_preps = {'beyond', 'from', 'off', 'out', 'via', 'ayond', 'ayont', 'froward', 'frowards',
                                'fromward', 'outwith'}

double_not_at_location_preps = {'far from', 'out from', 'out of', 'away from'}


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
        candidate_relations = build_candidate_relations_from_frames(json_parse_data)
        build_relations(dependencies, characters, candidate_relations)
        remove_location_preps(characters)
        all_characters.extend(characters)

    # Perform anaphora resolution of all types.
    resolve_anaphora(all_characters)
    for character in all_characters:
        print character

    return all_characters


# Remove location prepositions from characters texts and is_a relations
def remove_location_preps(characters):
    for character in characters:
        location_prep = has_location_prep(character.text)[0]
        character.text = character.text.replace(location_prep, '').strip()

        is_a_list = character.type_to_list['IsA']
        to_remove = None
        for is_a_rel in is_a_list:
            to_remove = is_a_rel
            break

        to_add = to_remove.replace(location_prep, '').strip()
        character.type_to_list['IsA'].remove(to_remove)
        character.type_to_list['IsA'].append(to_add)


# Add ConceptNet-style relations to character object based on the candidate relations derived from Semafor
#  and from heuristics of the dependency tree.
def build_relations(dependencies, characters, candidate_relations):
    for character in characters:
        for dependency in dependencies:
            if character.character_id == dependency['ID']:
                # Related dependencies are the ones that might create a relation for a particular character.
                related_dependencies = get_all_related_dependencies(dependency, dependencies, candidate_relations)
                for related_dependency in related_dependencies:
                    try:
                        # Check if Semafor found a relation, take it if it did since it is likely to be more accurate.
                        candidate_relation = candidate_relations[related_dependency[1]['FORM']]
                        form = related_dependency[1]['FORM']
                        negatives = [neg for neg in set(form.split(' ')) if neg in negative_words]
                        relation = ''
                        if len(negatives) % 2 == 1:
                            relation = 'Not'

                        if candidate_relation[1].startswith('Not') and relation:
                            relation_type = candidate_relation[1][3:]
                        else:
                            relation_type = relation + candidate_relation[1]

                        object_text = candidate_relation[2]

                        # Send message is a four tuple so we get the receiver and give them the message as well as
                        #  making the current character the sender
                        if relation_type == 'SendMessage':
                            message = candidate_relation[2]
                            character.add_relation(relation_type, message)
                            object_text = candidate_relation[3]
                            for char in characters:
                                if object_text in char.text or char.text in object_text:
                                    char.add_relation('ReceiveMessage', message)
                        else:
                            # If the object could not be deciphered by Semafor, we can take a guess.
                            if not object_text:
                                object_text = characters[characters.index(character)+1].text
                            character.add_relation(relation_type, object_text)
                        continue
                    except KeyError:
                        # If nothing for this word found by Semafor, try to find something using the dependencies
                        determine_relation_types(related_dependency, character)

    # Sometimes the related dependencies of an object earlier in a sentence overlaps with that of objects later in the
    #  same sentence (not usually the other way around).
    # This causes duplication and ultimately incorrect relations for the earlier object. So we arbitrarily remove any
    #  relations that earlier objects have that overlap with later objects.
    n = 1
    for character in characters:
        first_has_property = character.type_to_list['HasProperty']
        first_not_has_property = character.type_to_list['NotHasProperty']
        for i in range(n, len(characters)):
            second_has_property = characters[n].type_to_list['HasProperty']
            second_not_has_property = characters[n].type_to_list['NotHasProperty']
            for has_p in second_has_property:
                if has_p in first_has_property:
                    first_has_property.remove(has_p)
            for not_has_p in second_not_has_property:
                if not_has_p in first_not_has_property:
                    first_not_has_property.remove(not_has_p)
            n += 1


# Using the dependency relations only, find possible ConceptNet relations.
# See doc for meanings of each of the relations.
# If it is just a verb an doesn't match anything else, then we say that it was a TakeAction
def determine_relation_types(related_dependency, character):
    deprel = related_dependency[0]
    form = related_dependency[1]['FORM']
    postag = related_dependency[1]['POSTAG']
    negatives = [neg for neg in set(form.split(' ')) if neg in negative_words]
    relation = ''
    if len(negatives) % 2 == 1:
        relation = 'Not'
        words = form.split(' ')
        form = ' '.join(words[words.index(negatives[-1])+1:])

    if deprel == 'amod' or deprel == 'conj' or deprel == 'poss' or postag.startswith('J'):
        relation += 'HasProperty'
        character.add_relation(relation, form)

    elif deprel == 'agent' or deprel == 'nsubj' or deprel == 'prep' and form != 'that' \
            and not postag.startswith('P') and not postag.startswith('V'):
        location_prep = has_location_prep(form)
        if location_prep[0]:

            if not location_prep[1]:
                if relation:
                    relation = ''
                else:
                    relation = 'Not'

            relation += 'AtLocation'
            character.add_relation(relation, form)
        elif deprel != 'prep':
            relation += 'IsA'
            character.add_relation(relation, form)

    elif deprel == 'nsubjpass' or deprel == 'dobj':
        relation += 'ReceivesAction'
        character.add_relation(relation, form)
        
    elif deprel == 'xsubj' or deprel == 'rcmod':
        character.add_relation('CapableOf', form)

    elif related_dependency[1]['POSTAG'].startswith('V'):
        relation += 'TakesAction'
        character.add_relation(relation, form)


def has_location_prep(form):
    form_words = form.lstrip().split(' ')
    prep = ''
    positive = True

    # Try from the longest sequence first, for obvious reasons
    for triple_prep in triple_at_location_preps:
        if triple_prep in form:
            prep = triple_prep
            break

    if not prep:
        for double_prep in double_at_location_preps:
            if double_prep in form:
                prep = double_prep
                break

    if not prep:
        for double_not_prep in double_not_at_location_preps:
            if double_not_prep in form:
                prep = double_not_prep
                positive = False
                break

    if not prep:
        for single_prep in single_at_location_preps:
            if single_prep in form_words:
                prep = single_prep
                break

    if not prep:
        for single_not_prep in single_not_at_location_preps:
            if single_not_prep in form_words:
                prep = single_not_prep
                positive = False
                break

    return prep, positive

# We want everything to be character centric, so we use this to get all of the related dependencies to a character.
# Builds the spider diagram from the character chunk. Anything going out stays, anything coming in is reversed.
# Going out relations are transitive
# We also want all of the ones going out of the one that comes in, although this can lead to some duplication.
#   We handle this downstream though.
def get_all_related_dependencies(dependency, dependencies, candidate_relations):
    related_dependencies = []

    in_deps = get_in_dependencies(dependency, dependencies, candidate_relations)
    for in_dep in in_deps:
        related_dependencies.append(in_dep)

    out_deps = get_out_dependencies(dependency, dependencies, candidate_relations)
    for out_dep in out_deps:
        related_dependencies.append(out_dep)

    return related_dependencies


# Find all nodes going out (i.e. ID of current is same as HEAD of considered)
def get_out_dependencies(dependency, dependencies, candidate_relations):
    out_deps = []
    for dep in dependencies:
        if dep['HEAD'] == dependency['ID']:
                out_dep = dep['DEPREL'], dep
                out_deps.append(out_dep)
                out_deps.extend(get_out_dependencies(dep, dependencies, candidate_relations))

    return out_deps


# Find the (single) node coming in (i.e. HEAD of current is same as ID of considered)
# Recurse on the others going out of the one coming in
def get_in_dependencies(dependency, dependencies, candidate_relations):
    in_deps = []
    for dep in dependencies:
        if dep['ID'] == dependency['HEAD']:
            in_dep = dependency['DEPREL'], dep
            in_deps.append(in_dep)
            dependencies_without_this_one = dependencies
            dependencies_without_this_one.remove(dependency)
            in_deps.extend(get_out_dependencies(dep, dependencies_without_this_one, candidate_relations))

    return in_deps


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
    socket = urlopen(request_url)
    json = json_load(socket.read())
    socket.close()
    return json