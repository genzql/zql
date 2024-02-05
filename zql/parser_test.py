import pytest
from zql.parser import parse_to_ast, query_to_tokens, ZqlParserError


def test_query_to_tokens():
    raw = " HI\ni,   LIKE\rit "
    actual = query_to_tokens(raw)
    expected = ["hi", "i", ",", "like", "it"]
    assert actual == expected


def test_missing_select():
    with pytest.raises(ZqlParserError) as err:
        parse_to_ast("hello")
        
        actual = str(err.value)
        expected = "Expected `its giving`, not `hello`."
        assert actual == expected


def test_missing_select_expr():
    with pytest.raises(ZqlParserError) as err:
        parse_to_ast("its giving")
        
        actual = str(err.value)
        expected = "Expected expression, not ``."
        assert actual == expected


def test_missing_from_after_expr():
    with pytest.raises(ZqlParserError) as err:
        parse_to_ast("its giving a from")
        
        actual = str(err.value)
        expected = "Expected `yass`, not `from`."
        assert actual == expected


def test_missing_from_after_expr_list():
    with pytest.raises(ZqlParserError) as err:
        parse_to_ast("its giving a, b from")
        
        actual = str(err.value)
        expected = "Expected `yass`, not `from`."
        assert actual == expected


def test_missing_table():
    with pytest.raises(ZqlParserError) as err:
        parse_to_ast("its giving a yass")
        
        actual = str(err.value)
        expected = "Expected table, not ``."
        assert actual == expected


def test_missing_limit():
    with pytest.raises(ZqlParserError) as err:
        parse_to_ast("its giving a yass table say")
        
        actual = str(err.value)
        expected = "Expected `say less`, not `say`."
        assert actual == expected


def test_missing_limit_amount():
    with pytest.raises(ZqlParserError) as err:
        parse_to_ast("its giving a yass table say less")
        
        actual = str(err.value)
        expected = "Expected integer, not ``."
        assert actual == expected


def test_missing_limit_amount_integer():
    with pytest.raises(ZqlParserError) as err:
        parse_to_ast("its giving a yass table say less five")
        
        actual = str(err.value)
        expected = "Expected integer, not `five`."
        assert actual == expected


def test_missing_terminal():
    with pytest.raises(ZqlParserError) as err:
        parse_to_ast("its giving a yass table say less 5")
        
        actual = str(err.value)
        expected = "You're cappin bro. Expected no cap, not ``."
        assert actual == expected


def test_missing_terminal_full():
    with pytest.raises(ZqlParserError) as err:
        parse_to_ast("its giving a yass table say less 5 no")
        
        actual = str(err.value)
        expected = "You're cappin bro. Expected no cap, not `no`."
        assert actual == expected


def test_missing_select_expr_list():
    with pytest.raises(ZqlParserError) as err:
        parse_to_ast("its giving a,")
        
        actual = str(err.value)
        expected = "Expected expression, not ``."
        assert actual == expected


def test_parse_to_ast_simple_select():
    raw_query = """
    its giving a, b
    yass example
    no cap
    """
    actual = parse_to_ast(raw_query)
    expected = {
        "type": "query",
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
    assert actual == expected

def test_parse_to_ast_simple_select_with_limit():
    raw_query = """
    its giving a, b
    yass example
    say less 10
    no cap
    """
    actual = parse_to_ast(raw_query)
    expected = {
        "type": "query",
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
                "type": "keyword",
                "value": "LIMIT",
                "children": [{"type": "integer", "value": "10"}],
            },
            {
                "type": "terminal",
                "value": ";",
            },
        ]
    }
    assert actual == expected
