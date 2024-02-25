from zql.types import ZqlQuery, SqlQuery
from zql.parser import parse_to_ast
from zql.renderer import render_from_ast
from zql.grammar import parse_ast
from zql.grammar_loader import get_zql_grammar
from zql.grammar_renderer import render_query


ZQL_GRAMMAR = get_zql_grammar()


class Zql:
    """Converts ZQL queries to SQL."""

    def __init__(self):
        pass

    def parse(self, raw: ZqlQuery, use_grammar: bool = False) -> SqlQuery:
        if use_grammar:
            ast = parse_ast(ZQL_GRAMMAR, raw)
            sql = render_query(ast)
            return sql

        ast = parse_to_ast(raw)
        sql = render_from_ast(ast)
        return sql
