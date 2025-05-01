#!/usr/bin/env python3
"""
Command-line interface for PyGCA.
"""
import argparse
import ast
import os
import sys
from typing import List

from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker
from bot.bitwise.bitwise_checker import BitwiseOperatorChecker
from bot.comparison.comparison_checker import ComparisonOperatorChecker
from bot.identity_membership.identity_checker import IdentityOperatorChecker
from bot.identity_membership.membership_checker import MembershipOperatorChecker
from bot.logical.logical_checker import LogicalOperatorChecker
from bot.utils import set_parents


def analyze_file(file_path: str, checkers: List[str] = None) -> dict:
    """
    Analyze a Python file for operator issues.

    Args:
        file_path: Path to the Python file
        checkers: List of checkers to use (default: all)

    Returns:
        Dictionary of issues by checker
    """
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    tree = ast.parse(code)
    set_parents(tree)

    all_checkers = {
        "arithmetic": ArithmeticOperatorChecker(),
        "bitwise": BitwiseOperatorChecker(),
        "comparison": ComparisonOperatorChecker(),
        "identity": IdentityOperatorChecker(),
        "membership": MembershipOperatorChecker(),
        "logical": LogicalOperatorChecker(),
    }

    if not checkers:
        checkers = list(all_checkers.keys())

    results = {}
    for checker_name in checkers:
        if checker_name not in all_checkers:
            print(f"Warning: Unknown checker '{checker_name}'")
            continue

        checker = all_checkers[checker_name]
        checker.visit(tree)
        issues = checker.get_issues()
        if issues:
            results[checker_name] = issues

    return results


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="PyGCA - Python General Code Analyzer")
    parser.add_argument(
        "files", nargs="+", help="Python files or directories to analyze"
    )
    parser.add_argument(
        "--checkers",
        nargs="+",
        choices=[
            "arithmetic",
            "bitwise",
            "comparison",
            "identity",
            "membership",
            "logical",
        ],
        help="Specific checkers to run",
    )
    parser.add_argument("--output", "-o", help="Output file for results")

    args = parser.parse_args()

    all_results = {}

    for path in args.files:
        if os.path.isdir(path):
            # If path is a directory, scan all Python files
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        try:
                            results = analyze_file(file_path, args.checkers)
                            if results:
                                all_results[file_path] = results
                        except Exception as e:
                            print(f"Error analyzing {file_path}: {e}")
        else:
            # If path is a file, analyze it directly
            try:
                results = analyze_file(path, args.checkers)
                if results:
                    all_results[path] = results
            except Exception as e:
                print(f"Error analyzing {path}: {e}")

    # Output results
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            for file_path, issues_by_checker in all_results.items():
                f.write(f"File: {file_path}\n")
                for checker, issues in issues_by_checker.items():
                    f.write(f"  {checker.capitalize()} issues:\n")
                    for issue in issues:
                        f.write(f"    - {issue}\n")
                f.write("\n")
    else:
        for file_path, issues_by_checker in all_results.items():
            print(f"\nFile: {file_path}")
            for checker, issues in issues_by_checker.items():
                print(f"  {checker.capitalize()} issues:")
                for issue in issues:
                    print(f"    - {issue}")


if __name__ == "__main__":
    sys.exit(main())
