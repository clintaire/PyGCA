import ast
import textwrap
from bot.bitwise.bitwise_checker import BitwiseOperatorChecker
from bot.utils import set_parents

def test_bitwise_operator_detection():
    old_logic_code = textwrap.dedent("""
        def bitwise_operation():
            result = a & b  # Correct usage of bitwise AND
            result = a | b  # Correct usage of bitwise OR
            if a | b:  # Incorrect usage: bitwise OR in logical context
                return False
    """)

    new_logic_code = textwrap.dedent("""
        def bitwise_operation():
            result = a & b
            result = a ^ b  # Correct usage of bitwise XOR
            if a | b:  # Same incorrect usage as before
                return False
    """)

    tree_old = ast.parse(old_logic_code)
    set_parents(tree_old)
    checker_old = BitwiseOperatorChecker()
    checker_old.visit(tree_old)
    issues_old = checker_old.get_issues()
    assert len(issues_old) == 1  # Expect 1 issue in old logic

    tree_new = ast.parse(new_logic_code)
    set_parents(tree_new)
    checker_new = BitwiseOperatorChecker()
    checker_new.visit(tree_new)
    issues_new = checker_new.get_issues()
    assert len(issues_new) == 1  # Expect 1 issue in new logic