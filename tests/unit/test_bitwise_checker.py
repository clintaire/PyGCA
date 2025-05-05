import ast

from bot.bitwise.bitwise_checker import BitwiseOperatorChecker
from bot.utils import set_parents


def test_bitwise_operator_detection():
    old_logic_code = """
def bitwise_operation():
    result = a & b
    result = a | b
    if a | b:
        return False
    """
    new_logic_code = """
def bitwise_operation():
    result = a & b
    result = a ^ b
    if a | b:
        return False
    """
    tree_old = ast.parse(old_logic_code)
    set_parents(tree_old)
    checker_old = BitwiseOperatorChecker()
    checker_old.visit(tree_old)
    issues_old = checker_old.get_issues()
    assert len(issues_old) == 1, "Old logic code should have one issue"

    tree_new = ast.parse(new_logic_code)
    set_parents(tree_new)
    checker_new = BitwiseOperatorChecker()
    checker_new.visit(tree_new)
    issues_new = checker_new.get_issues()
    assert len(issues_new) == 1, "New logic code should have one issue"
