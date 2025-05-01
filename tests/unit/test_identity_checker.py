import ast
from bot.identity_membership.identity_checker import IdentityOperatorChecker
from bot.utils import set_parents


def test_identity_operator_detection():
    source_code = """
def identity_check():
    if a is b:
        return True
    if a is not b:
        return False
    """
    tree = ast.parse(source_code)
    set_parents(tree)
    checker = IdentityOperatorChecker()
    checker.visit(tree)
    issues = checker.get_issues()
    assert len(issues) == 2  # Expect 2 issues
