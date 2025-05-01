# PyGCA Usage Examples

[Back to Index](index.md) | [API Reference](api_reference.md)

This document provides practical examples of using PyGCA to analyze Python code for operator issues.

## Basic Usage

### Detecting Division by Zero

```python
import ast
from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker
from bot.utils import set_parents

# Sample code with division by zero
source_code = """
def calculate():
    a = 10
    b = 0
    return a / b  # Division by zero
"""

# Parse the code and set parent references
tree = ast.parse(source_code)
set_parents(tree)

# Check for arithmetic issues
checker = ArithmeticOperatorChecker()
checker.visit(tree)
issues = checker.get_issues()

# Print detected issues
print(issues)  # ['Division by zero at line 5']
```

### Detecting Bitwise Operator Misuse

```python
import ast
from bot.bitwise.bitwise_checker import BitwiseOperatorChecker
from bot.utils import set_parents

# Sample code with bitwise operator misuse in conditionals
source_code = """
def check_flags(a, b):
    if a | b:  # Potentially mistaken for logical OR
        return True
    return False
"""

# Parse the code and set parent references
tree = ast.parse(source_code)
set_parents(tree)

# Check for bitwise operator issues
checker = BitwiseOperatorChecker()
checker.visit(tree)
issues = checker.get_issues()

# Print detected issues
print(issues)  # ['Potential misuse of bitwise OR at line 3']
```

## Advanced Usage

### Scanning an Entire Repository

```python
from bot.operator_detection import analyze_repository, save_results

# Analyze all Python files in the repository
results = analyze_repository("/path/to/repository")

# Save results to a file
save_results("my_project", results)
```

### Combining Multiple Checkers

```python
import ast
from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker
from bot.comparison.comparison_checker import ComparisonOperatorChecker
from bot.bitwise.bitwise_checker import BitwiseOperatorChecker
from bot.utils import set_parents

# Sample code with multiple operator types
source_code = """
def multi_operator_function(a, b):
    c = a / 0  # Arithmetic issue
    if a == None:  # Comparison issue
        return a | b  # Bitwise issue in conditional
"""

# Parse the code and set parent references
tree = ast.parse(source_code)
set_parents(tree)

# Initialize checkers
arithmetic_checker = ArithmeticOperatorChecker()
comparison_checker = ComparisonOperatorChecker()
bitwise_checker = BitwiseOperatorChecker()

# Run all checkers on the same AST
arithmetic_checker.visit(tree)
comparison_checker.visit(tree)
bitwise_checker.visit(tree)

# Collect issues from all checkers
all_issues = (
    arithmetic_checker.get_issues() +
    comparison_checker.get_issues() +
    bitwise_checker.get_issues()
)

# Print all detected issues
for issue in all_issues:
    print(issue)
```

### Using Configuration Options

```python
import ast
from bot.config_parser import ConfigLoader
from bot.arithmetic.arithmetic_checker import check_arithmetic_operators

# Load configuration
config = ConfigLoader()
config.load_config()
excluded_files = config.get_excluded_files()

# Sample file path check
file_path = "path/to/file.py"
if any(excluded in file_path for excluded in excluded_files):
    print(f"Skipping {file_path} based on configuration")
else:
    with open(file_path, 'r') as f:
        code = f.read()
    issues = check_arithmetic_operators(code)
    print(f"Found {len(issues)} issues in {file_path}")
```

### Performance Profiling

```python
import time
import ast
import cProfile
import pstats
from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker
from bot.utils import set_parents

# Generate a large code sample
source_code = """
def large_function():
    x = 1
""" * 10000  # Replicate a small function 10,000 times

# Profile the performance
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
stats.sort_stats("cumulative")
stats.print_stats(10)

print(f"Analysis completed in {end_time - start_time:.4f} seconds")
```

## Customization Examples

### Creating a Custom Operator Checker

```python
import ast
from bot.base_operator_checker import BaseOperatorChecker

class CustomOperatorChecker(BaseOperatorChecker):
    def __init__(self):
        super().__init__()
        self.issues = []

    def visit_Call(self, node):
        """Check for issues in function calls."""
        if isinstance(node.func, ast.Name) and node.func.id == 'eval':
            self.issues.append(f"Potentially unsafe use of eval() at line {node.lineno}")
        self.generic_visit(node)

    def get_issues(self):
        return self.issues

# Example usage
source_code = """
def unsafe_function(user_input):
    return eval(user_input)  # Potentially unsafe
"""

tree = ast.parse(source_code)
checker = CustomOperatorChecker()
checker.visit(tree)
issues = checker.get_issues()
print(issues)  # ['Potentially unsafe use of eval() at line 3']
```
