"""Base class for operator checkers."""

import ast


class BaseOperatorChecker(ast.NodeVisitor):
    """Base class for all operator checkers."""

    def __init__(self):
        """Initialize the BaseOperatorChecker."""
        self.issues = []

    def log_issue(self, message, node):
        """Log an issue with line number information."""
        self.issues.append(f"{message} at line {node.lineno}")

    def get_issues(self):
        """Return the list of issues found."""
        return self.issues

    def check(self, tree):
        """Perform the check on an AST tree."""
        self.visit(tree)
        return self.get_issues()
