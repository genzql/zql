from zql.grammar import Grammar, parse_grammar


ZQL_GRAMMAR_PATH = "zql/zql_grammar.tmjd"


def get_zql_grammar() -> Grammar:
    with open(ZQL_GRAMMAR_PATH, "r") as file:
        content = file.read()
        return parse_grammar(content)