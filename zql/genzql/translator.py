from .grammar import Grammar
from .parser import parse_ast
from .renderer import render_query
from .types import MaybeDialect


def translate(
    grammar: Grammar,
    source: str,
    source_dialect: MaybeDialect = None,
    target_dialect: MaybeDialect = None
) -> str:
    ast = parse_ast(grammar, source, source_dialect)
    target = render_query(grammar, ast, target_dialect)
    return target