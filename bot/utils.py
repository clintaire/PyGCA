import ast

def set_parents(node, parent=None):
    """ Recursively set the parent attribute for AST nodes """
    node.parent = parent
    for child in ast.iter_child_nodes(node):
        set_parents(child, node)