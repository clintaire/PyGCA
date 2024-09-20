import ast

class ArithmeticOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_BinOp(self, node):
        # Detect potential misuse of arithmetic operators
        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            if isinstance(node.op, ast.Div):
                # Check for division by zero
                if isinstance(node.right, ast.Constant) and node.right.value == 0:
                    self.issues.append(f"Division by zero at line {node.lineno}")
            # Add more misuse detection logic if necessary
        self.generic_visit(node)

    def get_issues(self):
        return self.issues