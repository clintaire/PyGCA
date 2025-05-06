import ast
import os
import re
from pathlib import Path

# Assuming the bot has some functions to detect specific operator misuse, e.g.:
from bot.arithmetic.arithmetic_checker import check_arithmetic_operators
from bot.comparison.comparison_checker import check_comparison_operators

# Remove this line to fix the circular import
# from bot.operator_detection import check_operators


# Use check_operators directly if it's defined below in the same file
def check_operators(tree):
    """
    Example function to check operators in an AST tree.
    """
    # Implementation here...
    pass


# Add other necessary operator checks here


def analyze_repository(repo_path):
    """
    Analyze a repository for operator issues.
    """
    results = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()
                tree = ast.parse(code)
                arithmetic_issues = check_operators(tree)  # Example usage
                # Add issues to results
                results[file_path] = {"arithmetic_issues": arithmetic_issues}
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
            if issues.get("arithmetic_issues"):
                f.write("Arithmetic issues:\n")
                for line, issue in issues["arithmetic_issues"].items():
                    f.write(f"  Line {line}: {issue}\n")
            if issues.get("comparison_issues"):
                f.write("Comparison issues:\n")
                for line, issue in issues["comparison_issues"].items():
                    f.write(f"  Line {line}: {issue}\n")
            f.write("\n")
    print(f"Results saved to {output_file}")


save_results("test_repo", {"file.py": {}}, output_dir="results")
