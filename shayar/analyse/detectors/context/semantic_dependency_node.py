__author__ = 'Nitin'


class SemanticDependencyNode:

    def __init__(self, id, form, cpostag, postag):
        self.id = id
        self.form = form
        self.cpostag = cpostag
        self.postag = postag
        self.children = []
        self.deprel = {}      # Map of child node id and dependency relation to that node

    def add_child(self, deprel, child_node):
        self.deprel[child_node.id] = deprel
        self.children.append(child_node)

    def __str__(self):
        s = '{ ' + str(self.id) + ' '

        for child in self.children:
            s += str(child) + ' '

        return s + ' }'