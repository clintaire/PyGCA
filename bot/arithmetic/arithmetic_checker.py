import ast
from bot.config_parser import ConfigLoader

class ArithmeticOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []
        self.config = ConfigLoader().load_config()
        self.strict_mode = self.config.getboolean('arithmetic', 'strict_mode', fallback=False)

    def visit_BinOp(self, node):
        # Detect misuse of arithmetic operators
        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            if self.strict_mode:
                self.issues.append(f"Potential misuse of arithmetic operator at line {node.lineno}")
        self.generic_visit(node)

    def get_issues(self):
        return self.issues