# API Reference

[Back to Index](index.md) | [See Examples](examples.md)

This document provides detailed information about the PyGCA API, including all public classes and methods.

### Core Modules

#### Operator Checkers

PyGCA provides several specialized checker classes that analyze Python code for specific operator patterns and potential issues.

##### ArithmeticOperatorChecker

```python
from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker
```

A class that checks for arithmetic operator issues like division by zero.

**Methods**

- `__init__()`: Initialize a new checker instance
- `visit_BinOp(node)`: Visit binary operation nodes to check for arithmetic issues
- `get_issues()`: Return a list of detected issues

**Example**

```python
import ast
from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker
from bot.utils import set_parents

source_code = """
def calculate():
    a = 5
    b = 0
    c = a / b  # Division by zero
"""

tree = ast.parse(source_code)
set_parents(tree)
checker = ArithmeticOperatorChecker()
checker.visit(tree)
issues = checker.get_issues()
print(issues)  # ['Division by zero at line 4']
```

##### BitwiseOperatorChecker

```python
from bot.bitwise.bitwise_checker import BitwiseOperatorChecker
```

A class that checks for potential misuse of bitwise operators, especially in conditional statements.

**Methods**

- `__init__()`: Initialize a new checker instance
- `visit_BinOp(node)`: Visit binary operation nodes to check for bitwise issues
- `get_issues()`: Return a list of detected issues

##### ComparisonOperatorChecker

```python
from bot.comparison.comparison_checker import ComparisonOperatorChecker
```

A class that checks for comparison operator issues.

**Methods**

- `__init__()`: Initialize a new checker instance
- `visit_Compare(node)`: Visit comparison nodes to check for misuse
- `get_issues()`: Return a list of detected issues

##### IdentityOperatorChecker

```python
from bot.identity_membership.identity_checker import IdentityOperatorChecker
```

A class that checks for potential misuse of identity operators (`is`, `is not`).

**Methods**

- `__init__()`: Initialize a new checker instance
- `visit_Compare(node)`: Visit comparison nodes to check for identity operator misuse
- `get_issues()`: Return a list of detected issues

##### LogicalOperatorChecker

```python
from bot.logical.logical_checker import LogicalOperatorChecker
```

A class that checks for logical operator usage and potential issues in boolean expressions.

**Methods**

- `__init__()`: Initialize a new checker instance
- `visit_BoolOp(node)`: Visit boolean operation nodes to check for issues
- `get_issues()`: Return a list of detected issues

##### MembershipOperatorChecker

```python
from bot.identity_membership.membership_checker import MembershipOperatorChecker
```

A class that checks for potential misuse of membership operators (`in`, `not in`).

**Methods**

- `__init__()`: Initialize a new checker instance
- `visit_Compare(node)`: Visit comparison nodes to check for membership operator misuse
- `get_issues()`: Return a list of detected issues

### Utility Functions

#### set_parents

```python
from bot.utils import set_parents
```

A utility function to set parent references in an AST tree.

**Parameters**

- `node`: The root node of the AST tree

**Example**

```python
import ast
from bot.utils import set_parents

tree = ast.parse("a + b")
set_parents(tree)
```

#### configure_logging

```python
from bot.utils import configure_logging
```

Configures logging for the PyGCA library.

**Parameters**

- `level`: Logging level (default: `logging.INFO`)
- `fmt`: Log message format (default: `'%(asctime)s - %(name)s - %(levelname)s - %(message)s'`)

**Example**

```python
from bot.utils import configure_logging

configure_logging()
```

### Repository Analysis

#### analyze_repository

```python
from bot.operator_detection import analyze_repository
```

Analyzes all Python files in a repository for operator misuse.

**Parameters**

- `repo_path`: (str) Path to the repository root

**Returns**

- (dict) Mapping of file paths to dictionaries of issues

**Example**

```python
from bot.operator_detection import analyze_repository, save_results

results = analyze_repository("path/to/repository")
save_results("my_repo", results)
```

#### save_results

```python
from bot.operator_detection import save_results
```

Saves analysis results to a log file.

**Parameters**

- `repo_name`: (str) Name of the repository
- `results`: (dict) Analysis results from `analyze_repository`
- `output_dir`: (str) Directory to save results (default: "results")

**Example**

```python
from bot.operator_detection import analyze_repository, save_results

results = analyze_repository("path/to/repository")
save_results("my_repo", results)
```

### Configuration

#### ConfigLoader

```python
from bot.config_parser import ConfigLoader
```

Loads configuration from `.pygcconfig` file.

**Methods**

- `__init__(config_file='.pygcconfig')`: Initialize with specified config file
- `load_config()`: Load and return configuration
- `get_excluded_files()`: Get list of files to exclude
- `get_excluded_operators()`: Get list of operators to exclude
- `should_read_readme()`: Check if README should be parsed
- `should_read_contributing()`: Check if CONTRIBUTING should be parsed
- `get_custom_message(operator)`: Get custom message for an operator

**Example**

```python
from bot.config_parser import ConfigLoader

config = ConfigLoader()
config.load_config()
excluded_files = config.get_excluded_files()
```

#### GuidelineParser

```python
from bot.guideline_parser import GuidelineParser
```

Parses guidelines from README and CONTRIBUTING files.

**Methods**

- `__init__(readme_file='README.md', contributing_file='CONTRIBUTING.md')`: Initialize with specified files
- `parse_guidelines()`: Parse and return guidelines

**Example**

```python
from bot.guideline_parser import GuidelineParser

parser = GuidelineParser()
guidelines = parser.parse_guidelines()
```
