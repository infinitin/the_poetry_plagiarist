__author__ = 'Nitin'
from semantic_dependency_node import SemanticDependencyNode
from pattern.text.en import lemma as lemmatise
from nltk.corpus import wordnet

negative_adverbs = set(['not', 'seldom', 'hardly', 'barely', 'scarcely', 'rarely', 'vmod'])


def find_subject(root_node):
    if root_node.postag.startswith('N'):
        return root_node.character

    subj_branches = ['agent', 'nsubj']
    branches = root_node.deprel.keys()
    for branch in subj_branches:
        if branch in branches:
            return root_node.deprel[branch].character


def find_object(root_node):
    obj_branches = ['nsubjpass', 'dobj']
    branches = root_node.deprel.keys()
    for branch in obj_branches:
        if branch in branches:
            return root_node.deprel[branch].character


def build_relations(root_node):
    assert isinstance(root_node, SemanticDependencyNode)
    if root_node.candidate_relation:
        #if it has Syntax instructions, handle them first and then accept the candidate relation and move on
        for child in root_node.deprel.values():
            build_relations(child)
    else:
        branches = root_node.deprel.keys()
        type = root_node.postag

        word = root_node.form
        if 'dep' in branches:
            word = root_node.deprel['dep'].form + ' ' + word
        if 'measure' in branches:
            word = root_node.deprel['measure'].form + ' ' + word
        if 'num' in branches:
            word = root_node.deprel['num'].form + ' ' + word
        if 'number' in branches:
            word = root_node.deprel['number'].form + ' ' + word
        if 'preconj' in branches:
            word = root_node.deprel['preconj'].form + ' ' + word
        if 'predet' in branches:
            word = root_node.deprel['predet'].form + ' ' + word
        if 'quantmmod' in branches:
            word = root_node.deprel['quantmod'].form + ' ' + word
        if 'nn' in branches:
            word = root_node.deprel['nn'].form + ' ' + word
        if 'pobj' in branches:
            word = root_node.deprel['pobj'].form + ' ' + word


        subject = find_subject(root_node)
        if not subject:
            #Actually we want to get some of the universal relations checked.
            for child in root_node.deprel.values():
                build_relations(child)

        object = find_object(root_node)

        # See if there is a negative hanging around
        negative = 'neg' in branches
        if 'advmod' in branches:
            if lemmatise(root_node.deprel['advmod'].form) in negative_adverbs:
                negative = not negative
            else:
                try:
                    adjective = wordnet.lemmas(root_node.deprel['advmod'].form)[0].pertainyms()[0].name
                    relation = 'HasProperty' if not negative else 'NotHasProperty'
                    subject.add_relation(relation, adjective)
                except IndexError:
                    pass

        # HasProperty Relations mostly...
        if 'acomp' in branches:
            relation = 'HasProperty' if not negative else 'NotHasProperty'
            subject.add_relation(relation, root_node.deprel['acomp'].form + ' ' + word)

        if 'amod' in branches:
            relation = 'HasProperty' if not negative else 'NotHasProperty'
            subject.add_relation(relation, root_node.deprel['amod'].form)

        if 'conj' in branches:
            relation = 'HasProperty' if not negative else 'NotHasProperty'
            subject.add_relation(relation, root_node.deprel['conj'].form)

        if 'cop' in branches:
            if type.startswith('J'):
                relation = 'HasProperty' if not negative else 'NotHasProperty'
                subject.add_relation(relation, word)
            else:
                relation = 'IsA' if not negative else 'NotIsA'
                subject.add_relation(relation, word)

        if 'nsubjpass' in branches:
            relation = 'TakesAction' if not negative else 'NotTakesAction'
            subject.add_relation(relation, word)
            relation = 'ReceivesAction' if not negative else 'NotReceivesAction'
            object.add_relation(relation, word)

        if 'poss' in branches:
            relation = 'HasProperty' if not negative else 'NotHasProperty'
            subject.add_relation(relation, word)

        # Some AtLocation stuff
        if 'prep' in branches:
            relation = 'AtLocation' if not negative else 'NotAtLocation'

        # And finish off with a CapableOf
        if 'xsubj' in branches:
            relation = 'CapableOf' if not negative else 'NotCapableOf'
            subject.add_relation(relation, word)

        for child in root_node.deprel.values():
                build_relations(child)

        '''
        word = root_node.form
        if root_node.postag.startswith('V'):
            if lemmatise(word) in VERBNET_LEMMAS:
                # Find the character and the parameter and add the type that we already know
                # Check for negation adverbs
            else:
                # Look at the branches
                # If there is a subject and object, create a TakeAction and ReceiveAction respectfully
                # If only subject then TakeAction
                # If only object then ReceivesAction and HasProperty
                # Apply any adverbs to the subject of the relation as adjectives as mapped in wordnet
                # Check for negation adverbs
        else:
            # Look at the branches and do what they say...
        #see sheet
        return
        '''