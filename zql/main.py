from zql.types import ZqlQuery, SqlQuery
from zql.parser import parse_to_ast
from zql.renderer import render_from_ast


class Zql:
    """Converts ZQL queries to SQL."""

    def __init__(self):
        pass

    def parse(self, raw: ZqlQuery) -> SqlQuery:
        ast = parse_to_ast(raw)
        sql = render_from_ast(ast)
        return sql
