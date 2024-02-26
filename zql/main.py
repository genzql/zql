from zql.types import ZqlQuery, SqlQuery
from zql.parser import ZqlParserError, parse_to_ast
from zql.renderer import render_from_ast
from zql.grammar import AstParseError, parse_ast
from zql.grammar_loader import get_zql_grammar
from zql.grammar_renderer import QueryRenderError, render_query


ZQL_GRAMMAR = get_zql_grammar()


class Zql:
    """Converts ZQL queries to SQL."""

    def __init__(self):
        pass

    def parse(self, raw: ZqlQuery, use_grammar: bool = False) -> SqlQuery:
        if use_grammar:
            try:
                ast = parse_ast(ZQL_GRAMMAR, raw)
                sql = render_query(ZQL_GRAMMAR, ast)
                return sql
            except AstParseError as ape:
                raise ZqlParserError(ape)
            except QueryRenderError as qre:
                raise ZqlParserError(ape)

        ast = parse_to_ast(raw)
        sql = render_from_ast(ast)
        return sql
