#!/usr/bin/env python3
"""
Automated code quality checker for PyGCA.
Run this before committing code to ensure quality standards.
"""
import os
import subprocess
import sys


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n===== Running {description} =====")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{description} passed!")
    else:
        print(f"{description} failed!")
        print(result.stdout)
        print(result.stderr)
    return result.returncode == 0


def check_code():
    """Run all code quality checks."""
    all_passed = True

    # Run black via python -m
    black_cmd = [sys.executable, "-m", "black", "--check", "."]
    black_passed = run_command(black_cmd, "Black code formatter")
    all_passed = all_passed and black_passed

    # Run isort via python -m
    isort_cmd = [sys.executable, "-m", "isort", "--check", "--profile", "black", "."]
    isort_passed = run_command(isort_cmd, "isort import sorter")
    all_passed = all_passed and isort_passed

    # Run pylint via python -m
    pylint_cmd = [sys.executable, "-m", "pylint", "bot", "tests"]
    pylint_passed = run_command(pylint_cmd, "pylint code analysis")
    all_passed = all_passed and pylint_passed

    # Run mypy via python -m
    mypy_cmd = [sys.executable, "-m", "mypy", "bot"]
    mypy_passed = run_command(mypy_cmd, "mypy type checking")
    all_passed = all_passed and mypy_passed

    # Run pytest via python -m
    pytest_cmd = [sys.executable, "-m", "pytest"]
    pytest_passed = run_command(pytest_cmd, "pytest with coverage")
    all_passed = all_passed and pytest_passed

    if all_passed:
        print("\n✅ All checks passed!")
        return 0
    else:
        print("\n❌ Some checks failed. Please fix the issues.")
        return 1


if __name__ == "__main__":
    sys.exit(check_code())
