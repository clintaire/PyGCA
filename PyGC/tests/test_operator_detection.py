import pytest
from bot.comparison.comparison_checker import ComparisonOperatorChecker
import ast
import textwrap

def test_comparison_operator_detection():
    source_code = textwrap.dedent("""
        def compare():
            if a == b:
                return True
            elif a != b:
                return False
    """)
    
    tree = ast.parse(source_code)
    checker = ComparisonOperatorChecker()
    checker.visit(tree)
    issues = checker.get_issues()

    # Expect no issues since comparison operators are used correctly
    assert len(issues) == 0