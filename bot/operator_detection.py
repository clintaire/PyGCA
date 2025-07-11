"""Module for detecting operator patterns in Python code."""

import ast
import os
import re
from pathlib import Path

from bot.arithmetic.arithmetic_checker import check_arithmetic_operators
from bot.comparison.comparison_checker import check_comparison_operators


def analyze_repository(repo_path):
    """
    Analyze a repository for operator issues.

    Args:
        repo_path: Path to the repository to analyze

    Returns:
        Dictionary mapping file paths to their analysis results
    """
    results = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        code = f.read()

                    # Run different checkers
                    arithmetic_issues = check_arithmetic_operators(code)
                    comparison_issues = check_comparison_operators(code)

                    # Store results
                    file_results = {}
                    if arithmetic_issues:
                        file_results["arithmetic_issues"] = arithmetic_issues
                    if comparison_issues:
                        file_results["comparison_issues"] = comparison_issues

                    # Always add arithmetic_issues and comparison_issues keys for test compatibility
                    if "arithmetic_issues" not in file_results:
                        file_results["arithmetic_issues"] = []
                    if "comparison_issues" not in file_results:
                        file_results["comparison_issues"] = []

                    results[file_path] = file_results
                except (IOError, SyntaxError) as e:
                    # Skip files that can't be read or parsed
                    print(f"Warning: Could not analyze {file_path}: {e}")
                    continue
    return results


def sanitize_filename(filename: str) -> str:
    """
    Sanitize the filename to prevent path injection.
    Removes unsafe characters and replaces spaces with underscores.

    Args:
        filename: The input filename to sanitize.

    Returns:
        A sanitized filename.
    """
    # Remove unsafe characters and replace spaces with underscores
    return re.sub(r"[^\w\-_.]", "_", filename)


def save_results(repo_name, results, output_dir="results"):
    """
    Saves the analysis results to a log file.

    Args:
        repo_name: Name of the repository (used for the output file name).
        results: Dictionary containing analysis results.
        output_dir: Directory where the results file will be saved.
    """
    # Sanitize the repo_name to prevent path injection
    safe_repo_name = sanitize_filename(repo_name)

    # Ensure the output directory exists
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # Construct the output file path safely
    output_file = output_dir_path / f"{safe_repo_name}_results.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        for file_path, issues in results.items():
            f.write(f"File: {file_path}\n")

            # Handle arithmetic issues
            arithmetic_issues = issues.get("arithmetic_issues", [])
            if arithmetic_issues:
                f.write("Arithmetic issues:\n")
                for issue in arithmetic_issues:
                    f.write(f"  {issue}\n")

            # Handle comparison issues
            comparison_issues = issues.get("comparison_issues", [])
            if comparison_issues:
                f.write("Comparison issues:\n")
                for issue in comparison_issues:
                    f.write(f"  {issue}\n")
            f.write("\n")
    print(f"Results saved to {output_file}")
