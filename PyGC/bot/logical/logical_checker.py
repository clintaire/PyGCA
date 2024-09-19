import ast

class LogicalOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_BinOp(self, node):
        # Detect misuse of bitwise operators in logical contexts
        if isinstance(node.op, ast.BitOr):
            self.issues.append(f"Potential misuse of bitwise OR at line {node.lineno}")
        elif isinstance(node.op, ast.BitAnd):
            self.issues.append(f"Potential misuse of bitwise AND at line {node.lineno}")
        self.generic_visit(node)

    def get_issues(self):
        return self.issues