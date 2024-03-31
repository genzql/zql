from pathlib import Path
from .grammar import Grammar, parse_grammar


ZQL_GRAMMAR_PATH = Path(__file__).parent / "zql_grammar.tmjd"


def get_zql_grammar() -> Grammar:
    with ZQL_GRAMMAR_PATH.open("r") as file:
        content = file.read()
        return parse_grammar(content)