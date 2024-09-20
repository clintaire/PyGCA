import ast

class BitwiseOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_BinOp(self, node):
        # Detect misuse of bitwise OR (|), AND (&), XOR (^), and shift operators (<<, >>)
        if isinstance(node.op, ast.BitOr):
            self.check_misuse(node, "bitwise OR")
        elif isinstance(node.op, ast.BitAnd):
            self.check_misuse(node, "bitwise AND")
        elif isinstance(node.op, ast.BitXor):
            self.check_misuse(node, "bitwise XOR")
        elif isinstance(node.op, ast.LShift):
            self.check_misuse(node, "left shift (<<)")
        elif isinstance(node.op, ast.RShift):
            self.check_misuse(node, "right shift (>>)")
        self.generic_visit(node)

    def check_misuse(self, node, operator_name):
        # This method checks if a bitwise operator is used in a logical context
        parent = getattr(node, 'parent', None)
        if isinstance(parent, ast.If) or isinstance(parent, ast.BoolOp):
            self.issues.append(f"Potential misuse of {operator_name} at line {node.lineno}")
        elif isinstance(parent, ast.BinOp):
            # Recursively check for nested bitwise misuse
            self.check_misuse(parent, operator_name)

    def get_issues(self):
        return self.issues