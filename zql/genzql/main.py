from .types import ZqlQuery, SqlQuery
from .parser import AstParseError
from .loader import get_zql_grammar
from .renderer import QueryRenderError
from .translator import translate
from .types import MaybeDialect


ZQL_DIALECT = "zql"
TARGET_DIALECT = "sqlite"
ZQL_GRAMMAR = get_zql_grammar()


class ZqlParserError(Exception):
    pass


def get_dialect_from_name(name: str) -> MaybeDialect:
    if name == ZQL_DIALECT:
        return None
    return name


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

    def translate(self, raw: str, source: str, target: str) -> str:
        source_dialect = get_dialect_from_name(source)
        target_dialect = get_dialect_from_name(target)
        try:
            sql = translate(ZQL_GRAMMAR, raw, source_dialect, target_dialect)
            return sql
        except AstParseError as ape:
            raise ZqlParserError(ape)
        except QueryRenderError as qre:
            raise ZqlParserError(ape)