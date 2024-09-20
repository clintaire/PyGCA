import ast
import textwrap
from bot.identity_membership.identity_checker import IdentityOperatorChecker

def test_identity_operator_detection():
    # Old logic
    old_logic_code = textwrap.dedent("""
        def identity_check():
            if a is b:  # Correct usage
                return True
            if a is not b:  # Correct usage
                return False
    """)
    
    # New logic
    new_logic_code = textwrap.dedent("""
        def identity_check():
            if a is b:
                return True
            if a is not None:  # Correct usage
                return False
    """)

    # Test old logic
    tree_old = ast.parse(old_logic_code)
    checker_old = IdentityOperatorChecker()
    checker_old.visit(tree_old)
    issues_old = checker_old.get_issues()
    assert len(issues_old) == 0  # No issues in old logic

    # Test new logic
    tree_new = ast.parse(new_logic_code)
    checker_new = IdentityOperatorChecker()
    checker_new.visit(tree_new)
    issues_new = checker_new.get_issues()
    assert len(issues_new) == 0  # No issues in new logic