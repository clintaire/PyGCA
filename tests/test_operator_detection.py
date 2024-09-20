import ast
import textwrap
from bot.operator_detection import OperatorDetector
from bot.utils import set_parents

def test_combined_operator_detection():
    # Source code containing both arithmetic and bitwise operations
    source_code = textwrap.dedent("""
        def check_operators():
            a = 5
            b = 10

            # Arithmetic operations
            c = a + b  # Correct usage
            d = a / 0  # Division by zero, potential issue

            # Bitwise operations
            result = a & b  # Correct usage of bitwise AND
            if a | b:  # Incorrect usage: bitwise OR in logical context
                return False
    """)

    tree = ast.parse(source_code)
    set_parents(tree)  # Ensure parent nodes are set

    # Instantiate and run the OperatorDetector
    detector = OperatorDetector()
    detector.visit(tree)
    issues = detector.get_issues()

    # Assertions based on the issues found
    assert len(issues) == 2  # Expect two issues: division by zero and bitwise OR used in logical context