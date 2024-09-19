import ast
from bot.config_parser import ConfigLoader

class BitwiseOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []
        self.config = ConfigLoader().load_config()

    def visit_BinOp(self, node):
        # Detect misuse of bitwise operators
        if isinstance(node.op, ast.BitOr):  # Bitwise OR (|) used in logical context
            if isinstance(node.parent, ast.If):
                self.issues.append(f"Potential misuse of bitwise OR at line {node.lineno}")
        elif isinstance(node.op, ast.BitAnd):  # Bitwise AND (&) used in logical context
            if isinstance(node.parent, ast.If):
                self.issues.append(f"Potential misuse of bitwise AND at line {node.lineno}")
        self.generic_visit(node)

    def get_issues(self):
        return self.issues