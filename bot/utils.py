import ast

def set_parents(node):
    for child in ast.iter_child_nodes(node):
        child.parent = node
        set_parents(child)
