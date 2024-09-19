import ast
from bot.config_parser import ConfigLoader

class ComparisonOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []
        self.config = ConfigLoader().load_config()
        self.custom_message = self.config.get('comparison', 'custom_message', fallback=None)

    def visit_Compare(self, node):
        for op in node.ops:
            # Only apply the custom message if the comparison is with None
            if isinstance(op, ast.Eq) or isinstance(op, ast.NotEq):
                # Check if one of the operands is None
                if (isinstance(node.left, ast.Constant) and node.left.value is None) or \
                   (isinstance(node.comparators[0], ast.Constant) and node.comparators[0].value is None):
                    if self.custom_message:
                        self.issues.append(f"{self.custom_message} at line {node.lineno}")
                    else:
                        self.issues.append(f"Potential misuse of comparison operator at line {node.lineno}")
        self.generic_visit(node)

    def get_issues(self):
        return self.issues