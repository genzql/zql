import pytest
from zql.parser import AstParseError, parse_ast
from zql.sample_grammars import FORMULA_GRAMMAR, LIST_GRAMMAR


def test_parse_ast_formula_simple():
    actual = parse_ast(FORMULA_GRAMMAR, "7 * c")
    expected = {
        "type": "formula",
        "children": [
            {
                "type": "expr",
                "children": [
                    {"type": "number", "value": "7"}
                ],
            },
            {
                "type": "operator",
                "value": "*"
            },
            {
                "type": "expr",
                "children": [
                    {"type": "word", "value": "c"}
                ],
            },
        ],
    }
    assert actual == expected
    

def test_parse_ast_formula_nested():
    actual = parse_ast(FORMULA_GRAMMAR, "(A + 12) - 0")

    expected = {
        "type": "formula",
        "children": [
            {
                "type": "expr",
                "children": [
                    {"type": "open", "value": "("},
                    {
                        "type": "formula",
                        "children": [
                            {
                                "type": "expr",
                                "children": [
                                    {"type": "word", "value": "A"}
                                ],
                            },
                            {
                                "type": "operator",
                                "value": "+"
                            },
                            {
                                "type": "expr",
                                "children": [
                                    {"type": "number", "value": "12"}
                                ],
                            },
                        ],
                    },
                    {"type": "close", "value": ")"},
                ],
            },
            {"type": "operator", "value": "-"},
            {
                "type": "expr",
                "children": [
                    {"type": "number", "value": "0"}
                ],
            },
        ],
    }
    assert actual == expected


def test_parse_ast_formula_fail_first_token():
    with pytest.raises(AstParseError) as err:
        parse_ast(FORMULA_GRAMMAR, "_7 * c")
    actual = str(err.value)
    expected = "Expected `_7` to match `[0-9]+`."
    assert actual == expected


def test_parse_ast_formula_fail_unparsed_tokens_remain():
    with pytest.raises(AstParseError) as err:
        parse_ast(FORMULA_GRAMMAR, "7 * c + 3")
    actual = str(err.value)
    expected = "Could not apply `root` rule to remaining tokens: ['+', '3']"
    assert actual == expected


def test_parse_ast_formula_fail_no_source():
    with pytest.raises(AstParseError) as err:
        parse_ast(FORMULA_GRAMMAR, "")
    actual = str(err.value)
    expected = "Expected match for `[0-9]+`, not end of input."
    assert actual == expected


def test_parse_ast_list_simple():
    actual = parse_ast(LIST_GRAMMAR, "1, 2 0")
    expected = {
        "type": "list",
        "children": [
            {
                "type": "num_list",
                "children": [
                    {"type": "num", "value": "1"},
                    {"type": "comma", "value": ","},
                    {
                        "type": "num_list",
                        "children": [
                            {"type": "num", "value": "2"},
                        ],
                    },
                ],
            },
            {"type": "end", "value": "0"},
        ],
    }
    assert actual == expected