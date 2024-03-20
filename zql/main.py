from zql.types import ZqlQuery, SqlQuery
from zql.parser import AstParseError
from zql.loader import get_zql_grammar
from zql.renderer import QueryRenderError
from zql.translator import translate


TARGET_DIALECT = "sqlite"
ZQL_GRAMMAR = get_zql_grammar()


class ZqlParserError(Exception):
    pass


class Zql:
    """Converts ZQL queries to SQL."""

    def __init__(self):
        pass

    def parse(self, raw: ZqlQuery) -> SqlQuery:
        try:
            sql = translate(ZQL_GRAMMAR, raw, target_dialect=TARGET_DIALECT)
            return sql
        except AstParseError as ape:
            raise ZqlParserError(ape)
        except QueryRenderError as qre:
            raise ZqlParserError(ape)
