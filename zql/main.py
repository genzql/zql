from zql.types import ZqlQuery, SqlQuery
from zql.parser import AstParseError, parse_ast
from zql.loader import get_zql_grammar
from zql.renderer import QueryRenderError, render_query


ZQL_GRAMMAR = get_zql_grammar()


class ZqlParserError(Exception):
    pass


class Zql:
    """Converts ZQL queries to SQL."""

    def __init__(self):
        pass

    def parse(self, raw: ZqlQuery) -> SqlQuery:
        try:
            ast = parse_ast(ZQL_GRAMMAR, raw)
            sql = render_query(ZQL_GRAMMAR, ast)
            return sql
        except AstParseError as ape:
            raise ZqlParserError(ape)
        except QueryRenderError as qre:
            raise ZqlParserError(ape)
