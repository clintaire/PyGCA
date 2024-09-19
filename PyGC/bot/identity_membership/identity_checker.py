import ast

class IdentityOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Compare(self, node):
        for op in node.ops:
            if isinstance(op, ast.Is) or isinstance(op, ast.IsNot):
                # Check if comparing non-identity objects (e.g., integers or strings)
                if isinstance(node.left, (ast.Constant, ast.Num, ast.Str)) or isinstance(node.comparators[0], (ast.Constant, ast.Num, ast.Str)):
                    self.issues.append(f"Potential misuse of '{op}' at line {node.lineno}")
        self.generic_visit(node)

    def get_issues(self):
        return self.issues