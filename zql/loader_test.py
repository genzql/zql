from zql.loader import get_zql_grammar


def test_parse_zql_grammar():
    grammar = get_zql_grammar()
    assert grammar.get("root") is not None
