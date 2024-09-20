import ast
import textwrap
from bot.comparison.comparison_checker import ComparisonOperatorChecker

def test_comparison_operator_detection():
    # Old logic
    old_logic_code = textwrap.dedent("""
        def compare():
            if a == b:
                return True
            elif a != b:
                return False
    """)
    
    # New logic
    new_logic_code = textwrap.dedent("""
        def compare():
            if a == b:
                return True
            elif a > b:
                return False
    """)

    # Test old logic
    tree_old = ast.parse(old_logic_code)
    checker_old = ComparisonOperatorChecker()
    checker_old.visit(tree_old)
    issues_old = checker_old.get_issues()
    assert len(issues_old) == 0  # No issues expected in old logic

    # Test new logic
    tree_new = ast.parse(new_logic_code)
    checker_new = ComparisonOperatorChecker()
    checker_new.visit(tree_new)
    issues_new = checker_new.get_issues()
    assert len(issues_new) == 0  # No issues expected in new logic