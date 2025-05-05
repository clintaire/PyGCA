#!/usr/bin/env python3
"""
Command-line interface for PyGCA.

This module provides the command-line interface for the Python General Code Analyzer,
allowing users to scan Python files for various operator issues and other code quality
concerns.
"""
import argparse
import ast
import os
import sys
from typing import Dict, List, Optional

from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker
from bot.bitwise.bitwise_checker import BitwiseOperatorChecker
from bot.comparison.comparison_checker import ComparisonOperatorChecker
from bot.identity_membership.identity_checker import IdentityOperatorChecker
from bot.identity_membership.membership_checker import MembershipOperatorChecker
from bot.logical.logical_checker import LogicalOperatorChecker
from bot.utils import set_parents


class AnalysisError(Exception):
    """Base exception for analysis errors."""
    pass


class ParseError(AnalysisError):
    """Exception raised when parsing a Python file fails."""
    pass


class CheckerError(AnalysisError):
    """Exception raised when a checker encounters an error."""
    pass


def analyze_file(file_path: str, checkers: List[str] = None) -> Dict[str, List[str]]:
    """
    Analyze a Python file for operator issues.

    Args:
        file_path: Path to the Python file
        checkers: List of checkers to use (default: all)

    Returns:
        Dictionary of issues by checker

    Raises:
        FileNotFoundError: If the file does not exist
        ParseError: If the file cannot be parsed as Python code
        CheckerError: If a checker encounters an error
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except IOError as err:
        raise AnalysisError(f"I/O error reading file {file_path}: {err}")

    try:
        tree = ast.parse(code)
    except SyntaxError as err:
        raise ParseError(f"Syntax error in {file_path}: {err}")

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
        try:
            checker.visit(tree)
            issues = checker.get_issues()
            if issues:
                results[checker_name] = issues
        except Exception as err:
            raise CheckerError(f"Error in {checker_name} checker: {err}")

    return results


def main() -> int:
    """
    Main CLI function.

    Parses command-line arguments, runs the analysis on specified files,
    and outputs the results.

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
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
    error_count = 0
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
                        except FileNotFoundError as err:
                            print(f"File not found: {err}")
                            error_count += 1
                        except ParseError as err:
                            print(f"Parse error: {err}")
                            error_count += 1
                        except CheckerError as err:
                            print(f"Checker error: {err}")
                            error_count += 1
                        except Exception as err:
                            print(f"Unexpected error analyzing {file_path}: {err}")
                            error_count += 1
        else:
            # If path is a file, analyze it directly
            try:
                results = analyze_file(path, args.checkers)
                if results:
                    all_results[path] = results
            except FileNotFoundError as err:
                print(f"File not found: {err}")
                error_count += 1
            except ParseError as err:
                print(f"Parse error: {err}")
                error_count += 1
            except CheckerError as err:
                print(f"Checker error: {err}")
                error_count += 1
            except Exception as err:
                print(f"Unexpected error analyzing {path}: {err}")
                error_count += 1

    # Output results
    if all_results:
        try:
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
        except IOError as err:
            print(f"Error writing output: {err}")
            return 1

    return error_count


if __name__ == "__main__":
    sys.exit(main())
