import ast


class MembershipOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Compare(self, node):
        for op in node.ops:
            if isinstance(op, (ast.In, ast.NotIn)):
                if isinstance(node.left, ast.Constant):
                    op_name = "in" if isinstance(op, ast.In) else "not in"
                    self.issues.append(
                        f"Potential misuse of '{op_name}' at line {node.lineno}"
                    )
        self.generic_visit(node)

    def get_issues(self):
        return self.issues
