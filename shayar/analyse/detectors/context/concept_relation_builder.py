__author__ = 'Nitin'
from semantic_dependency_node import SemanticDependencyNode


def build_relations(root_node):
    assert isinstance(root_node, SemanticDependencyNode)
    if root_node.candidate_relation:
        #if it has Syntax instructions, handle them first and then accept the candidate relation and move on
        for child in root_node.children:
            return build_relations(child)
    else:
        #see sheet
        return