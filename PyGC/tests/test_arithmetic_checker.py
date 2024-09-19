import pytest
from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker
import ast
import textwrap

def test_arithmetic_operator_detection():
    source_code = textwrap.dedent("""
        def calculate():
            a = 5
            b = a + 2
            c = a * 10
    """)
    
    tree = ast.parse(source_code)
    checker = ArithmeticOperatorChecker()
    checker.visit(tree)
    issues = checker.get_issues()

    # Expect no misuse
    assert len(issues) == 0