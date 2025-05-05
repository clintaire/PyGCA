"""Module docstring for base_operator_checker."""


class BaseOperatorChecker:
    """Class docstring for BaseOperatorChecker."""

    def __init__(self):
        """Initialize the BaseOperatorChecker."""
        self.issues = []

    def log_issue(self, message, node):
        self.issues.append(f"{message} at line {node.lineno}")

    def get_issues(self):
        return self.issues

    def generic_visit(self, node):
        """Can be extended for future needs."""
        pass

    def check(self):
        """Perform the check."""
        pass  # Replace with actual implementation
