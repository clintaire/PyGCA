#!/usr/bin/env python3
"""
Automated test runner for PyGCA with coverage and reports.
"""
import os
import subprocess
import sys
import time
import webbrowser


def run_tests():
    """
    Run all tests with coverage and generate reports.
    """
    print("===== Running PyGCA Tests =====")

    # Create directories for reports if they don't exist
    if not os.path.exists("reports"):
        os.makedirs("reports")
    if not os.path.exists("reports/coverage"):
        os.makedirs("reports/coverage")

    start_time = time.time()

    # Run tests with coverage and generate reports
    cmd = [
        "pytest",
        "-v",
        "--cov=bot",
        "--cov-report=xml:reports/coverage.xml",
        "--cov-report=html:reports/coverage",
        "--junitxml=reports/test_results.xml",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Display test output
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)

    end_time = time.time()
    print(f"\nTests completed in {end_time - start_time:.2f} seconds")
    print(f"Return code: {result.returncode}")

    # Open coverage report in browser if tests passed
    if result.returncode == 0:
        coverage_report = os.path.abspath("reports/coverage/index.html")
        print(f"Opening coverage report: {coverage_report}")
        try:
            webbrowser.open(f"file://{coverage_report}")
        except Exception as e:
            print(f"Failed to open browser: {e}")

    return result.returncode


if __name__ == "__main__":
    sys.exit(run_tests())
