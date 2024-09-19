import pytest
from bot.bitwise.bitwise_checker import BitwiseOperatorChecker
from bot.utils import set_parents
import ast
import textwrap

def test_bitwise_operator_detection():
    source_code = textwrap.dedent("""
        def bitwise_operation():
            result = a & b  # Correct usage
            result = a | b  # Correct usage
            if a | b:  # Incorrect usage: bitwise OR in logical context
                return False
    """)
    
    tree = ast.parse(source_code)
    set_parents(tree)  # Ensure parent nodes are set
    checker = BitwiseOperatorChecker()
    checker.visit(tree)
    issues = checker.get_issues()

    # Expect one issue
    assert len(issues) == 1