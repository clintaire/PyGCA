<p align="center">
  <h2 align="center">PYGCA</h2>
  <p align="center">A static analysis tool that detects and analyzes operator usage patterns in Python codebases<p>
  <p align="center">
    <a href="https://github.com/clintaire/PyGCA/actions">
        <img src="https://img.shields.io/github/actions/workflow/status/clintaire/PyGCA/test.yml?branch=main&style=flat&colorA=0a0a0a&colorB=44CC11" alt="Build Status" />
    </a>
    <a href="https://pypistats.org/packages/PyGCA">
        <img src="https://img.shields.io/pypi/dm/PyGCA?style=flat&colorA=0a0a0a&colorB=FF8811" alt="Downloads" />
    </a>
    <a href="https://codecov.io/gh/clintaire/PyGCA">
        <img src="https://img.shields.io/codecov/c/github/clintaire/PyGCA?style=flat&colorA=0a0a0a&colorB=1285FD" alt="Coverage" />
    </a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat&colorA=0a0a0a" alt="License" />
    </a>
    <a href="https://github.com/psf/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat&colorA=0a0a0a" alt="Code Style" />
    </a>
    <a href="https://pypi.org/project/PyGCA/">
        <img src="https://img.shields.io/pypi/pyversions/PyGCA?style=flat&colorA=0a0a0a" alt="Python Versions" />
    </a>
  </p>
</p>

<br>

## Motivation

PyGCA was created to help developers contribute to open-source projects more efficiently by identifying minor code issues (like typos and naming convention inconsistencies) without having to manually review millions of lines of code. [Read more about our motivation and philosophy](docs/motivation.md).

## Table of Contents

- [Motivation](#motivation)
- [Table of Contents](#table-of-contents)
- [Key Features](#key-features)
- [Installation](#installation)
  - [From PyPI](#from-pypi)
  - [From Source](#from-source)
- [Quick Start](#quick-start)
  - [Basic Usage](#basic-usage)
  - [Example Analysis](#example-analysis)
- [Advanced Usage](#advanced-usage)
  - [Targeted Analysis](#targeted-analysis)
  - [Configuration](#configuration)
  - [Performance Profiling](#performance-profiling)
- [Testing](#testing)
- [Contributing](#contributing)
- [Documentation](#documentation)
- [Comparison with Similar Tools](#comparison-with-similar-tools)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
- [License](#license)
- [Real-world Use Cases](#real-world-use-cases)
- [Roadmap](#roadmap)

## Key Features

- 🎯 **Multi-operator detection** with specialized checkers
- 📝 **Actionable suggestions** with line-number references
- ⚙️ **Customizable rules** via `.pygcconfig` files
- 📊 **Performance profiling** for large codebases
- 📄 **Detailed reports** in multiple formats

## Installation

### From PyPI

```bash
pip install pygca
```

### From Source

```bash
git clone https://github.com/clintaire/PyGCA.git
cd PyGCA
pip install -e .
```

## Quick Start

### Basic Usage

Analyze a Python file:

```bash
python -m pygca analyze path/to/your_script.py
```

Sample output:

```
Found 3 potential issues in path/to/your_script.py:
1. [Line 5] Division by zero risk in 'a / 0'
2. [Line 8] Bitwise AND in conditional context
3. [Line 12] None comparison using '=='
```

### Example Analysis

Consider this sample code:

```python
def example(a, b):
    # Arithmetic operation
    result = a / 0

    # Bitwise in conditional
    if a & b:
        return True

    # Identity check
    return result is None
```

PyGCA would detect:

1. Potential division by zero
2. Bitwise operator in conditional context
3. Safe identity check (no issue)

## Advanced Usage

### Targeted Analysis

Check specific operator categories:

```bash
python -m pygca analyze --operators arithmetic,bitwise example.py
```

### Configuration

Create `.pygcconfig` in your project root:

```ini
[operators]
exclude_files = tests/, legacy/
exclude_categories = identity

[messages]
division_by_zero = "Custom warning: Possible division by zero at {line}"
```

### Performance Profiling

Analyze large codebases with resource monitoring:

```bash
python -m pygca analyze --profile large_project/
```

Sample profile output:

```
Processed 152 files (2.1MB) in 4.8s
Memory usage: 48.2MB peak
CPU utilization: 32%
```

## Testing

Run the test suite:

```bash
pytest tests/ --cov=pygca --cov-report=term-missing
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

See our [Contribution Guidelines](CONTRIBUTING.md) for details.

## Documentation

For full documentation and API reference, visit:

- [API Reference](docs/api_reference.md)
- [Usage Examples](docs/examples.md)
- [Configuration Guide](docs/configuration.md)

## Comparison with Similar Tools

| Feature       | PyGCA | Pylint | Flake8 |
| ------------- | ----- | ------ | ------ |
| Python 3.12+  | ✅     | ✅      | ✅      |
| Custom Rules  | High  | Medium | Low    |
| CLI Interface | ✅     | ✅      | ✅      |
| Plugin System | ❌     | ✅      | ✅      |

## Troubleshooting

### Common Issues

1. **ImportError when running PyGCA**
   - Make sure you've installed all dependencies with `pip install -r requirements.txt`

2. **False positives in operator detection**
   - Configure exclusions in your `.pygcconfig` file

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Real-world Use Cases

- **CI/CD Integration**: Automatically check PRs for operator issues
- **Large Codebase Migration**: Identify potential bugs when upgrading Python versions
- **Teaching Tool**: Help new developers understand operator nuances

## Roadmap

- [ ] Support for Python 3.12 match/case statements
- [ ] IDE integrations (VS Code, PyCharm)
- [ ] Web interface for online analysis
