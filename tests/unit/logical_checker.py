import ast

from bot.logical.logical_checker import LogicalOperatorChecker
from bot.utils import set_parents


def test_logical_operator_detection():
    source_code = """
def logical_operations():
    if a and b:
        return True
    if a or b:
        return False
    """
    tree = ast.parse(source_code)
    set_parents(tree)
    checker = LogicalOperatorChecker()
    checker.visit(tree)
    issues = checker.get_issues()
    assert len(issues) == 2  # Expect 2 issues for 'and' and 'or'
