from zql.grammar import parse_grammar
from zql.sample_grammars import FORMULA_GRAMMAR_CONTENT, LIST_GRAMMAR_CONTENT


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