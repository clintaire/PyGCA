import ast

class OperatorDetector(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_BinOp(self, node):
        # Detect division by zero
        if isinstance(node.op, ast.Div):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                self.issues.append(f"Division by zero at line {node.lineno}")
        
        # Detect misuse of bitwise OR in logical context
        if isinstance(node.op, ast.BitOr):
            if hasattr(node, 'parent') and isinstance(node.parent, ast.If):
                self.issues.append(f"Potential misuse of bitwise OR at line {node.lineno}")

        # Ensure to call generic_visit so that other nodes are visited properly
        self.generic_visit(node)

    def get_issues(self):
        # Return a unique list of issues to avoid duplicates
        return list(set(self.issues))

# Ensure the 'set_parents' function is setting parent attributes correctly.
def set_parents(node):
    for child in ast.iter_child_nodes(node):
        child.parent = node
        set_parents(child)