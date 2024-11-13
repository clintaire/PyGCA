import ast

class ArithmeticOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_BinOp(self, node):
        # Detect misuse of arithmetic operators (e.g., division by zero)
        if isinstance(node.op, ast.Div):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                self.issues.append(f"Division by zero at line {node.lineno}")
        self.generic_visit(node)

    def get_issues(self):
        return self.issues

def check_arithmetic_operators(code):
    checker = ArithmeticOperatorChecker()
    checker.visit(ast.parse(code))
    return checker.get_issues()