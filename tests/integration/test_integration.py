import ast

from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker
from bot.comparison.comparison_checker import ComparisonOperatorChecker
from bot.utils import set_parents


def test_combined_checkers():
    source_code = """
def test_function():
    a = 5
    b = a + 10
    if a == b:
        return True
    """
    tree = ast.parse(source_code)
    set_parents(tree)

    arithmetic_checker = ArithmeticOperatorChecker()
    comparison_checker = ComparisonOperatorChecker()

    arithmetic_checker.visit(tree)
    comparison_checker.visit(tree)

    assert len(arithmetic_checker.get_issues()) == 0
    assert len(comparison_checker.get_issues()) == 1
