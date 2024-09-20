import ast

def set_parents(node, parent=None):
    """
    Recursively set parent attributes for each node in the AST.
    """
    node.parent = parent
    for child in ast.iter_child_nodes(node):
        set_parents(child, node)