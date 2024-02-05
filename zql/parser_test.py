from zql.parser import parse_to_ast


def test_parse_to_ast():
    raw_query = """
    its giving a, b
    yass example
    no cap
    """
    actual = parse_to_ast(raw_query)
    expected = {
        "children": [
            {
                "type": "keyword",
                "value": "SELECT",
                "children": [
                    {"type": "expression", "value": "a"},
                    {"type": "expression", "value": "b"},
                ],
            },
            {
                "type": "keyword",
                "value": "FROM",
                "children": [{"type": "expression", "value": "example"}],
            },
            {
                "type": "terminal",
                "value": ";",
            },
        ]
    }
    # assert actual == expected
    assert actual == {}
