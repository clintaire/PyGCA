import ast


class ComparisonOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Compare(self, node):
        # Check for comparison with None using == instead of is
        for i, op in enumerate(node.ops):
            if isinstance(op, ast.Eq):
                # Check if comparing with None
                if i < len(node.comparators):
                    comparator = node.comparators[i]
                    if (
                        isinstance(comparator, ast.Constant)
                        and comparator.value is None
                    ):
                        self.issues.append(
                            f"Use 'is' instead of '==' when comparing with None at line {node.lineno}"
                        )
                # Also check if the left side is None
                if isinstance(node.left, ast.Constant) and node.left.value is None:
                    self.issues.append(
                        f"Use 'is' instead of '==' when comparing with None at line {node.lineno}"
                    )
        self.generic_visit(node)

    def get_issues(self):
        return self.issues


def check_comparison_operators(code):
    checker = ComparisonOperatorChecker()
    checker.visit(ast.parse(code))
    return checker.get_issues()
