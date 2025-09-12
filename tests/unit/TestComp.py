import ast

from bot.Comp.CompChk import ComparisonOperatorChecker
from bot.utils import set_parents


def test_comparison_operator_detection():
    source_code = """
def compare_values(a, b):
    if a == b:
        return True
    if a != b:
        return False
    """
    tree = ast.parse(source_code)
    set_parents(tree)
    checker = ComparisonOperatorChecker()
    checker.visit(tree)
    issues = checker.get_issues()
    assert len(issues) == 1, "Expect 1 issue"
