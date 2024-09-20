import ast
import textwrap
from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker

def test_arithmetic_operator_detection():
    # Old logic
    old_logic_code = textwrap.dedent("""
        def calculate():
            a = 5
            b = a + 2  # Correct usage of arithmetic operator
            c = a - 3  # Correct usage of arithmetic operator
            d = a * b  # Correct usage of arithmetic operator
    """)
    
    # New logic
    new_logic_code = textwrap.dedent("""
        def calculate():
            a = 5
            b = a + 2
            c = a * (5 - b)  # Correct usage
            d = a / 0  # Division by zero, potential issue
    """)

    # Test old logic
    tree_old = ast.parse(old_logic_code)
    checker_old = ArithmeticOperatorChecker()
    checker_old.visit(tree_old)
    issues_old = checker_old.get_issues()
    assert len(issues_old) == 0  # No issues expected in old logic

    # Test new logic
    tree_new = ast.parse(new_logic_code)
    checker_new = ArithmeticOperatorChecker()
    checker_new.visit(tree_new)
    issues_new = checker_new.get_issues()
    assert len(issues_new) == 1  # Expect issue with division by zero