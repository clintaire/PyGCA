import ast
import logging
from typing import List

logging.basicConfig(level=logging.INFO)


class ArithmeticOperatorChecker(ast.NodeVisitor):
    def __init__(self) -> None:
        self.issues: List[str] = []
        self.visited_nodes = set()

    def visit_BinOp(self, node: ast.BinOp) -> None:
        if id(node) in self.visited_nodes:
            return
        self.visited_nodes.add(id(node))

        if isinstance(node.op, ast.Div):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                issue = f"Division by zero at line {node.lineno}"
                logging.warning(issue)
                self.issues.append(issue)
        self.generic_visit(node)

    def get_issues(self) -> List[str]:
        return self.issues


def check_arithmetic_operators(code: str) -> List[str]:
    checker = ArithmeticOperatorChecker()
    checker.visit(ast.parse(code))
    return checker.get_issues()
