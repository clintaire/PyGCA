import ast
import textwrap
from bot.identity_membership.membership_checker import MembershipOperatorChecker

def test_membership_operator_detection():
    # Old logic
    old_logic_code = textwrap.dedent("""
        def membership_check():
            if a in b:  # Correct usage
                return True
            if a not in b:  # Correct usage
                return False
    """)
    
    # New logic
    new_logic_code = textwrap.dedent("""
        def membership_check():
            if a in b:
                return True
            if a not in b:
                return False
    """)

    # Test old logic
    tree_old = ast.parse(old_logic_code)
    checker_old = MembershipOperatorChecker()
    checker_old.visit(tree_old)
    issues_old = checker_old.get_issues()
    assert len(issues_old) == 0  # No issues in old logic

    # Test new logic
    tree_new = ast.parse(new_logic_code)
    checker_new = MembershipOperatorChecker()
    checker_new.visit(tree_new)
    issues_new = checker_new.get_issues()
    assert len(issues_new) == 0  # No issues in new logic