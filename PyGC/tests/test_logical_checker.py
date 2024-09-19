import pytest
from bot.logical.logical_checker import LogicalOperatorChecker
import ast
import textwrap

def test_logical_operator_detection():
    source_code = textwrap.dedent("""
        def logical_operation():
            if a and b:
                return True
            if a or b:
                return False
            if a | b:  # Incorrect usage: bitwise OR instead of logical OR
                return False
    """)
    
    tree = ast.parse(source_code)
    checker = LogicalOperatorChecker()
    checker.visit(tree)
    issues = checker.get_issues()

    # Expect one issue
    assert len(issues) == 1