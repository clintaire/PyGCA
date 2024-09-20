import ast
import textwrap
from bot.logical.logical_checker import LogicalOperatorChecker

def test_logical_operator_detection():
    # Old logic
    old_logic_code = textwrap.dedent("""
        def logical_operation():
            if a and b:
                return True
            if a or b:
                return False
            if a | b:  # Incorrect usage: bitwise OR instead of logical OR
                return False
    """)
    
    # New logic
    new_logic_code = textwrap.dedent("""
        def logical_operation():
            if a and b:
                return True
            if not (a or b):
                return False
            if a & b:  # Incorrect usage: bitwise AND instead of logical AND
                return False
    """)

    # Test old logic
    tree_old = ast.parse(old_logic_code)
    checker_old = LogicalOperatorChecker()
    checker_old.visit(tree_old)
    issues_old = checker_old.get_issues()
    assert len(issues_old) == 1  # 1 issue for bitwise OR used incorrectly

    # Test new logic
    tree_new = ast.parse(new_logic_code)
    checker_new = LogicalOperatorChecker()
    checker_new.visit(tree_new)
    issues_new = checker_new.get_issues()
    assert len(issues_new) == 1  # 1 issue for bitwise AND used incorrectly