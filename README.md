# Python Operator Detection & Analysis ' PYGC

## Overview
PyGC is a Python library designed to detect, analyze, and optimize the usage of operators in Python codebases. This tool ensures proper and efficient operator use, highlights potential misuse, and helps prevent performance issues or code vulnerabilities.

The tool covers major operator categories, offering insight into how different operators work together and where potential optimizations can occur.

## Key Features
- **Multi-operator detection**:
  - Arithmetic (`+`, `-`, `*`, `/`, etc.)
  - Bitwise (`&`, `|`, `^`, etc.)
  - Comparison (`==`, `!=`, `>`, etc.)
  - Identity (`is`, `is not`)
  - Logical (`and`, `or`, `not`)
  - Membership (`in`, `not in`)
- **Actionable suggestions** for performance improvements
- **Detailed reporting** on operator misuse
- **Customizable settings** for different project needs

> [!TIP]
> To better understand the __functional__ areas of each operator category and where they overlap, the following  diagram visually represents the __scope__ of PyGC:

```plaintext
      +----------------------------+
      |        Logical Operators   |
      |                            |
      |                            |      +---------------------------+
      | +---------+    +---------+ |      |                           |
      | | Bitwise |--> |Comparison |      |   Arithmetic Operators    |
      | +---------+    +---------+ |      |                           |
      |                            |      +---------------------------+
      +----------------------------+  
                                   |
                            +------+---------------------+
                            | Identity & Membership Ops  |
                            +----------------------------+
```
## [Go __to__ Installation](#installation)

1. Clone the `repository`:
```shell
   git clone https://github.com/clintaire/PyGC.git
   cd PyGC
```
2. `Install` dependencies:
```shell
   pip install -r requirements.txt
```

## Usage

__Run__ the __Operator__ Analysis

You can analyze __any__ Python script for __operator__ usage with a simple __command__:

```shell
   python3 -m bot.operator_analysis path/to/your_script.py
```
Here’s a basic Python script with various operators that __PyGC__ can analyze:

```python
    def analyze_example(a, b):
    # Arithmetic operators
    sum_result = a + b
    diff = a - b
    
    # Logical operators
    if a and b:
        return True
    elif a or b:
        return False

    # Bitwise operators
    result = a & b
    return result
```

Run PyGC and Inspect Output / __Basically__ to inspect the code above
> python3 -m bot.operator_analysis analyze_example.py

__Sample__ Output:
> ["Arithmetic Addition detected at line 4", "Logical AND detected at line 7", "Bitwise AND detected at line 12"]

__The following truth table demonstrates logical operator results and their detection by PyGC:__

|       Expression        |       Expected Result            |     Detected Issue     |
| ----------------------- | -------------------------------- | ---------------------- |
|    True and False       |      False                       |    No issue            |
|    False or True        |      True                        |    No issue            |
|    True and False       |      Data                        |    No issue            |
|    not True             |      False                       |    No issue            |
|    a and not b          |      Depends on vars             |    No issue            |
|    a & b (bitwise AND)  |      Depends on bits             |   🔴 Misuse _Alert_    |


> [!NOTE]
> You can modify PyGC’s behavior to handle special cases or focus on specific operator categories. To run only the arithmetic or comparison checks, you can adjust configuration files or pass custom flags during execution

__To only check for Arithmetic Operators__
>python3 -m bot.operator_analysis --check-arithmetic path/to/script.py


- When running PyGC on a larger codebase or a real-world project, it’s important to use modular analysis and profiling techniques to measure performance impact. Here’s how to profile the performance:

```python
   import time
   from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker
   from bot.utils import set_parents
   import ast

   # Load large source code
   source_code = """
   def large_function():
    x = 1
   """ * 10000  # Replicate a small function 10,000 times

   # Time the performance
   start_time = time.time()
   tree = ast.parse(source_code)
   set_parents(tree)
   checker = ArithmeticOperatorChecker()
   checker.visit(tree)
   end_time = time.time()

   print(f"Analysis completed in {end_time - start_time} seconds")
```
Running the above :top: code will allow you to test PyGC on __large__ scripts, and the output will help measure its __efficiency__.

# Testing

To ensure everything is working, you can run _PyGC’s_ test suite using pytest. This will validate the detection algorithms against various test cases:

>PYTHONPATH=. pytest tests/


## LICENSE

Copyright 2024-present Clint Airé.

The [PYGC](https://github.com/clintaire/mypy) repository is released under the [MIT](https://github.com/clintaire/mypy/blob/main/LICENSE.md) license.