import ast

from bot.identity_membership.membership_checker import MembershipOperatorChecker
from bot.utils import set_parents


def test_membership_operator_detection():
    source_code = """
def check_membership(a):
    elements = [1, 2, 3]
    if a in elements:
        return True
    if a not in elements:
        return False
    """
    tree = ast.parse(source_code)
    set_parents(tree)
    checker = MembershipOperatorChecker()
    checker.visit(tree)
    issues = checker.get_issues()
    assert len(issues) == 0  # No issues detected
