import pytest
from bot.identity_membership.membership_checker import MembershipOperatorChecker
import ast
import textwrap

def test_membership_operator_detection():
    source_code = textwrap.dedent("""
        def membership_check():
            if a in b:  # Correct usage
                return True
            if a not in b:  # Correct usage
                return False
    """)
    
    tree = ast.parse(source_code)
    checker = MembershipOperatorChecker()
    checker.visit(tree)
    issues = checker.get_issues()

    # Expect no misuse
    assert len(issues) == 0