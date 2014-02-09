__author__ = 'Nitin'


class CharacterDependencyNode:

    def __init__(self, id, form, cpostag, postag, character):
        self.id = id
        self.form = form
        self.cpostag = cpostag
        self.postag = postag
        self.character = None           # Related Character object
        self.dependencies = []          # Map of dependency relation to child node
        self.candidate_relation = ()    # Possible candidate relation found from framenet with this as the opword

    def add_child(self, relation, child_node):
        self.deprel[relation] = child_node

    def add_character(self, character):
        self.character = character
        
    def add_candidate_relation(self, candidate_relation):
        self.candidate_relation = candidate_relation

    def __str__(self):
        s = '{ ' + str(self.id) + ' '

        for child in self.children:
            s += str(child) + ' '

        return s + ' }'