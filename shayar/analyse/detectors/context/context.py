__author__ = 'Nitin'

from pattern.text.en import parsetree
from nltk.corpus import verbnet
from urllib2 import urlopen
from shayar.character import Character
#from is_a import find_is_a_relations
from at_location import find_at_location_relations
from has_a import find_has_a_relations
from json import loads as json_load
from semantic_dependency_node import SemanticDependencyNode

characters = []
relation_extractor = {}


def build_story(poem):
    lines = ""
    for line in poem:
        lines += line.lower() + " "

    parse_sentences = parsetree(lines, tags=True, chunks=True, relations=True, lemmata=True, tagset=True)

    sentences = [sentence.string for sentence in parse_sentences]

    for sentence in sentences:
        dependencies = get_dependencies(sentence)
        #Find the root.
        root = [dep for dep in dependencies if dep['HEAD'] == '0'][0]
        root_node = build_semantic_dependency_tree(dependencies, root)
        print str(root_node)


def build_semantic_dependency_tree(dependencies, root):
    root_node = SemanticDependencyNode(root['ID'], root['FORM'], root['CPOSTAG'], root['POSTAG'])
    children = [dep for dep in dependencies if dep['HEAD'] == root['ID']]

    for child in children:
        child_node = build_semantic_dependency_tree(dependencies, child)
        root_node.add_child(child['DEPREL'], child_node)

    return root_node


def get_dependencies(sentence):
    url = "http://demo.ark.cs.cmu.edu/parse/api/v1/parse?sentence="
    request_url = url + sentence.replace(' ', '+')
    socket = urlopen(request_url)
    json = json_load(socket.read())
    socket.close()
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


def build_relation_extractor():
    #Get the list of words that are like 'is'
    is_a_verbs = set(verbnet.lemmas('seem-109-1-1'))

    #Get the list of verbs where the subject owns the item
    hold_verbs = set(verbnet.lemmas('hold-15.1-1'))
    sustain_verbs = set(verbnet.lemmas('sustain-55.6'))
    keep_verbs = set(verbnet.lemmas('keep-15.2')).remove('leave')
    own_verbs = set(verbnet.lemmas('own-100'))
    steal_verbs = set(verbnet.lemmas('steal-10.5-1')).add('bring')
    equip_verbs = set(verbnet.lemmas('equip-13.4.2-1'))
    get_verbs = set(verbnet.lemmas('get-13.5.1-1'))
    obtain_verbs = set(verbnet.lemmas('obtain-13.5.2').extend(verbnet.lemmas('obtain-13.5.2-1'))).remove('select')
    hire_verbs = set(verbnet.lemmas('hire-13.5.3'))
    adopt_verbs = set(verbnet.lemmas('adopt-93'))
    use_verbs = set(verbnet.lemmas('use-105'))
    has_verbs_list = [hold_verbs, sustain_verbs, keep_verbs, own_verbs, steal_verbs, equip_verbs, get_verbs,
                      obtain_verbs, hire_verbs, adopt_verbs, use_verbs]
    has_verbs = frozenset().union(*has_verbs_list)

    #Put it in the relation extractor
    for is_a_verb in is_a_verbs:
        relation_extractor[is_a_verb] = find_is_a_relations

    for has_verb in has_verbs:
        relation_extractor[has_verb] = find_has_a_relations


def analyse_sentence(sentence):
    #get all the verbs
    verbs = set([word for word in sentence if word.type.startswith('V')])

    #send to the particular extractor with index of the chunk of the word
    for verb in verbs:
        try:
            relation_extractor[verb.lemma](sentence, sentence.chunks.index(sentence.words[sentence.words.index(verb)].chunk))
        except KeyError:
            print "This is where you send to the Take and Receive action extractors"


    #is_a_relations = find_is_a_relations(sentence)
    #for relation in is_a_relations:
    #    print relation

    #at_location_relations = find_at_location_relations(sentence)
    #for relation in at_location_relations:
    #    print relation


#def find_capable_of_relations(sentence):


#def determine_if_has_a_is_part_of_relation(hasA_relations):


#def find_receives_action_relations(sentence):



#def find_used_for_relations(sentence):



#def find_created_by_relations(sentence):



#def find_desires_relations(sentence):



#def find_has_property_relations(sentence):



#def resolve_characters():


"""
def build_drs(poem):
    #parser = load_parser('file:' + grammar_dir.replace('\\', '/'), trace=0, fstruct_parser=FeatStructParser(fdict_class=FeatStructNonterminal, logic_parser=DrtParser()))
    parser = load_parser('file:' + grammar_dir.replace('\\', '/'), trace=0, logic_parser=DrtParser())

    lines = ""
    for line in poem:
        lines += line + " "

    parse_sentences = parsetree(lines, tags=True, chunks=True, relations=True, lammata=True, tagset=True)

    accepted_types = ['JJ', 'JJR', 'JJS', 'MD', 'NN', 'NNP', 'NNPS', 'NNS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP','VBZ'   ]

    for sentence in parse_sentences:
        words = []
        for word in sentence.words:
            if word.type in accepted_types:
                words.extend(word)
        if not sentence.subjects:
            line = ""
            for word in words:
                line += word.string
            reparse_line = parsetree(lines, tags=True, chunks=True, relations=True, lammata=True, tagset=True)[0]
            words = []
            for reparse_word in reparse_line:
                words.extend(reparse_word)


    parse_sentences = parsetree(new_lines, tags=True, chunks=True, relations=True, lammata=True, tagset=True)


    #trees = parser.nbest_parse(line)
    trees = parser.nbest_parse('the bartender said the neutron'.split())
    if not trees: print 'no way to parse this!'
    for tree in trees:
        print(tree.node['SEM'].simplify())
"""