from zql.grammar import parse_grammar


ZLQ_GRAMMAR_PATH = "zql/zql_grammar.tmjd"


def test_parse_zql_grammar():
    with open(ZLQ_GRAMMAR_PATH, "r") as file:
        content = file.read()
        grammar = parse_grammar(content)

        assert grammar.get("root") is not None
