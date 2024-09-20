import ast

class IdentityOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Compare(self, node):
        # Detect misuse of identity operators
        for op in node.ops:
            if isinstance(op, ast.Is) or isinstance(op, ast.IsNot):
                if isinstance(node.left, ast.Constant) and node.left.value is None:
                    self.issues.append(f"Potential misuse of '{op}' at line {node.lineno}")
        self.generic_visit(node)

    def get_issues(self):
        return self.issues