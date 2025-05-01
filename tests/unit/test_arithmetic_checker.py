import ast
from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker
from bot.utils import set_parents


def test_arithmetic_operator_detection():
    old_logic_code = """
def calculate():
    a = 5
    b = a + 2
    c = a - 3
    d = a * b
    """
    new_logic_code = """
def calculate():
    a = 5
    b = a + 2
    c = a * (5 - b)
    d = a / 0  # Division by zero
    """
    tree_old = ast.parse(old_logic_code)
    set_parents(tree_old)
    checker_old = ArithmeticOperatorChecker()
    checker_old.visit(tree_old)
    issues_old = checker_old.get_issues()
    assert len(issues_old) == 0, "Old logic code should have no issues"

    tree_new = ast.parse(new_logic_code)
    set_parents(tree_new)
    checker_new = ArithmeticOperatorChecker()
    checker_new.visit(tree_new)
    issues_new = checker_new.get_issues()
    assert (
        len(issues_new) == 1
    ), "New logic code should have one issue (division by zero)"
    assert issues_new[0] == "Division by zero at line 6"
