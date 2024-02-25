from zql.grammar import AstNode
from zql.types import SqlQuery


def render_query(ast: AstNode) -> SqlQuery:
    raise NotImplementedError()
