import ast


class MembershipOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Compare(self, node):
        for op in node.ops:
            if isinstance(op, (ast.In, ast.NotIn)):
                if isinstance(node.left, ast.Constant):
                    self.issues.append(
                        f"Potential misuse of '{op}' at line {node.lineno}"
                    )
        self.generic_visit(node)

    def visit_BinOp(self, node):
        if isinstance(node.op, ast.In):
            if isinstance(node.left, ast.Constant):
                self.issues.append(
                    f"Potential misuse of 'in' operator at line {node.lineno}"
                )
        self.generic_visit(node)

    def get_issues(self):
        return self.issues
