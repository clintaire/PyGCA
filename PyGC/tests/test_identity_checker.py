import pytest
from bot.identity_membership.identity_checker import IdentityOperatorChecker
import ast
import textwrap

def test_identity_operator_detection():
    source_code = textwrap.dedent("""
        def identity_check():
            if a is b:  # Correct usage
                return True
            if a is not b:  # Correct usage
                return False
    """)
    
    tree = ast.parse(source_code)
    checker = IdentityOperatorChecker()
    checker.visit(tree)
    issues = checker.get_issues()

    # Expect no misuse
    assert len(issues) == 0