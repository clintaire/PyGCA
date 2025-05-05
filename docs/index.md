# PyGCA Documentation

Welcome to the **PyGCA** (Python General Code Analyzer) documentation! This guide provides an overview of the library, its features, and how to use it effectively.

## Overview

**PyGCA** is a code analysis tool designed to detect and analyze operator usage in Python codebases. It helps identify potential issues and misuses of various operators, improving code quality and preventing bugs.

The library scans Python code using the Abstract Syntax Tree (AST) and checks for issues with:

- **Arithmetic operators** (`+`, `-`, `*`, `/`, etc.) - Detecting issues like division by zero
- **Bitwise operators** (`&`, `|`, `^`, etc.) - Identifying confusion between bitwise and logical operations
- **Comparison operators** (`==`, `!=`, `>`, etc.) - Finding incorrect comparisons
- **Identity operators** (`is`, `is not`) - Detecting misuse compared to equality operators
- **Logical operators** (`and`, `or`, `not`) - Analyzing logical expressions
- **Membership operators** (`in`, `not in`) - Identifying potential performance issues

## Getting Started

### Installation

1. Clone the repository:

```bash
git clone https://github.com/clintaire/PyGCA.git
cd PyGCA
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install in development mode:

```bash
pip install -e .
```

## Quick Start

Here's a simple example to analyze a Python file for arithmetic operator issues:

```python
import ast
from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker
from bot.utils import set_parents

# Sample code with division by zero
code = """
def calculate():
    return 10 / 0  # Division by zero
"""

# Parse the code and analyze
tree = ast.parse(code)
set_parents(tree)
checker = ArithmeticOperatorChecker()
checker.visit(tree)

# Get and print issues
issues = checker.get_issues()
for issue in issues:
    print(issue)
```

### Documentation

[API Reference](api_reference.md) | [Usage Examples](examples.md)

## Key Features

PyGCA offers several key features:

- **Multi-operator detection**
  - Detects issues across different operator categories
  - Provides specialized checkers for each operator type

- **Actionable suggestions**
  - Offers clear feedback on operator misuse
  - Provides line numbers for easy issue location

- **Customizable settings**
  - Configure which operators and files to analyze
  - Define custom guidelines and messages

- **Performance profiling**
  - Built-in performance testing
  - Handles large codebases efficiently

## Configuration

PyGCA can be configured using a `.pygcconfig` file:

```ini
[operators]
exclude_files = tests/, examples/
exclude_operators = bitwise, identity

[guidelines]
read_readme = true
read_contributing = true

[comparison]
custom_message = "Please avoid using '==' for comparison with None. Use 'is' instead."
```

## Testing

Run the test suite to verify PyGCA works correctly:

```bash
pytest
```

For test coverage information:

```bash
pytest --cov=bot
```

## Contributing

Contributions are welcome! See the [CONTRIBUTING Guide](CONTRIBUTING.md) for more information.
