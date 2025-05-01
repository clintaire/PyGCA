import ast
import cProfile
import pstats
import time

from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker
from bot.bitwise.bitwise_checker import BitwiseOperatorChecker
from bot.comparison.comparison_checker import ComparisonOperatorChecker
from bot.identity_membership.identity_checker import IdentityOperatorChecker
from bot.identity_membership.membership_checker import MembershipOperatorChecker
from bot.logical.logical_checker import LogicalOperatorChecker
from bot.utils import set_parents


def test_combined_operator_detection():
    source_code = """
def check_operators():
    a = 5
    b = 10
    c = a + b
    d = a / 0  # Division by zero
    result = a & b
    if a | b:
        return False
    """
    tree = ast.parse(source_code)
    set_parents(tree)
    detector = ArithmeticOperatorChecker()
    detector.visit(tree)
    issues = detector.get_issues()
    assert len(issues) == 1  # Detects division by zero


def test_empty_function():
    source_code = """
def empty_function():
    pass
    """
    tree = ast.parse(source_code)
    set_parents(tree)
    checker = ArithmeticOperatorChecker()
    checker.visit(tree)
    issues = checker.get_issues()
    assert len(issues) == 0  # No issues in empty function


def test_large_strings_in_membership():
    source_code = f"""
def check_large_string():
    large_string = "{'a' * 10000}"
    if 'a' in large_string:
        return True
    """
    tree = ast.parse(source_code)
    set_parents(tree)
    checker = MembershipOperatorChecker()
    checker.visit(tree)
    issues = checker.get_issues()

    # Expecting the MembershipOperatorChecker to flag the membership check in a large string
    assert len(issues) == 1  # Adjust based on expected behavior of the checker


def test_performance_large_code():
    source_code = (
        """
def large_function():
    x = 1
    """
        * 10000
    )  # Replicate a small function 10,000 times

    profiler = cProfile.Profile()
    profiler.enable()

    start_time = time.time()
    tree = ast.parse(source_code)
    set_parents(tree)
    checker = ArithmeticOperatorChecker()
    checker.visit(tree)
    end_time = time.time()

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative").print_stats(10)

    execution_time = end_time - start_time
    assert execution_time < 1  # Ensure detection completes in under 1 second
