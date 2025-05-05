# filepath: c:\Users\focus\Documents\GitHub\PyGCA\bot\utils.py
import ast
import logging


def set_parents(node):
    for child in ast.iter_child_nodes(node):
        child.parent = node
        set_parents(child)


def configure_logging():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
