import pytest
from zql.grammar import AstParseError, get_tokens, parse_grammar, parse_ast


FORMULA_GRAMMAR_CONTENT = r"""
    root     : formula
             ;
    formula  : expr operator expr
             | expr
             ;
    expr     : open formula close
             | word
             | number
             ;
    open     : "("
             > "(\n"
             ;
    close    : ")"
             > "\n)"
             ;
    word     : r[a-zA-Z][\w$]*
             ;
    number   : r[0-9]+
             ;
    operator : "+"
             | "-"
             | "*"
             | "/"
             ;
"""
FORMULA_GRAMMAR = parse_grammar(FORMULA_GRAMMAR_CONTENT)


def test_get_tokens():
    source = """
    (A + 12) - 0
    """
    actual = get_tokens(source)
    expected = ["(", "A", "+", "12", ")", "-", "0"]
    assert actual == expected


def test_parse_grammar_formula():
    actual = parse_grammar(FORMULA_GRAMMAR_CONTENT)
    expected = {
        "root": [
            {"sequence": ["formula"]},
        ],
        "formula": [
            {"sequence": ["expr", "operator", "expr"]},
            {"sequence": ["expr"]},
        ],
        "expr": [
            {"sequence": ["open", "formula", "close"]},
            {"sequence": ["word"]},
            {"sequence": ["number"]},
        ],
        "open": [
            {"literal": "(", "template": "(\n"},
        ],
        "close": [
            {"literal": ")", "template": "\n)"},
        ],
        "word": [
            {"regex": r"[a-zA-Z][\w$]*"},
        ],
        "number": [
            {"regex": r"[0-9]+"},
        ],
        "operator": [
            {"literal": "+"},
            {"literal": "-"},
            {"literal": "*"},
            {"literal": "/"},
        ],
    }
    assert actual == expected


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
    expected = "Satisfied `root` rule, but unparsed tokens remain: ['+', '3']"
    assert actual == expected


def test_parse_ast_formula_fail_no_source():
    with pytest.raises(AstParseError) as err:
        parse_ast(FORMULA_GRAMMAR, "")
    actual = str(err.value)
    expected = "Expected match for `[0-9]+`, not end of input."
    assert actual == expected


LIST_GRAMMAR_CONTENT = r"""
root     : list
         ;
list     : num_list end
         ;
num_list : num comma num_list
         | num
         ;
num      : r[0-9]+
         ;
comma    : ","
         ;
end      : r[0-9]+
         ;
"""
LIST_GRAMMAR = parse_grammar(LIST_GRAMMAR_CONTENT)


def test_parse_grammar_list():
    actual = parse_grammar(LIST_GRAMMAR_CONTENT)
    expected = {
        "root": [
            {"sequence": ["list"]},
        ],
        "list": [
            {"sequence": ["num_list", "end"]},
        ],
        "num_list": [
            {"sequence": ["num", "comma", "num_list"]},
            {"sequence": ["num"]},
        ],
        "num": [
            {"regex": r"[0-9]+"},
        ],
        "comma": [
            {"literal": ","},
        ],
        "end": [
            {"regex": r"[0-9]+"},
        ],
    }
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
