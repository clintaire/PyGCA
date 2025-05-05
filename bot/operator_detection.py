import os

# Assuming the bot has some functions to detect specific operator misuse, e.g.:
from bot.arithmetic.arithmetic_checker import check_arithmetic_operators
from bot.comparison.comparison_checker import check_comparison_operators
from bot.operator_detection import check_operators

# Add other necessary operator checks here


def analyze_repository(repo_path):
    """
    Scans all Python files in the repository for operator misuse and outputs results locally.
    """
    results = {}

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    code = f.read()

                # Assuming each checker returns issues found in the format: {"line_number": "issue_description"}
                arithmetic_issues = check_arithmetic_operators(code)
                comparison_issues = check_comparison_operators(code)

                # Add issues to results
                if arithmetic_issues or comparison_issues:
                    results[file_path] = {
                        "arithmetic_issues": arithmetic_issues,
                        "comparison_issues": comparison_issues,
                    }

    return results


def save_results(repo_name, results, output_dir="results"):
    """
    Saves the analysis results to a log file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, f"{repo_name}_results.txt")

    with open(output_file, "w") as f:
        for file_path, issues in results.items():
            f.write(f"File: {file_path}\n")
            if issues["arithmetic_issues"]:
                f.write("Arithmetic issues:\n")
                for line, issue in issues["arithmetic_issues"].items():
                    f.write(f"  Line {line}: {issue}\n")
            if issues["comparison_issues"]:
                f.write("Comparison issues:\n")
                for line, issue in issues["comparison_issues"].items():
                    f.write(f"  Line {line}: {issue}\n")
            f.write("\n")
    print(f"Results saved to {output_file}")
