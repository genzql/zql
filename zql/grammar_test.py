from zql.grammar import parse_grammar
from zql.sample_grammars import (
    ENGLISH_TRANSLATION_GRAMMAR_CONTENT,
    FORMULA_GRAMMAR_CONTENT,
    LIST_GRAMMAR_CONTENT,
)


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
            {"literal": "(", "templates": [{"template": "(\n"}]},
        ],
        "close": [
            {"literal": ")", "templates": [{"template": "\n)"}]},
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


def test_parse_grammar_english():
    actual = parse_grammar(ENGLISH_TRANSLATION_GRAMMAR_CONTENT)
    expected = {
        "root": [
            {"sequence": ["english"]},
        ],
        "english": [
            {"sequence": ["sentence"]},
        ],
        "sentence": [
            {
                "sequence": ["name", "hello"],
                "dialects": ["yoda"],
                "templates": [
                    {"template": "{name} {hello}", "dialects": ["yoda"]},
                    {"template": "{hello} {name}"}
                ]
            },
            {
                "sequence": ["hello", "name"],
                "templates": [
                    {"template": "{name} {hello}", "dialects": ["yoda"]},
                    {"template": "{hello} {name}"}
                ]
            },
        ],
        "name": [
            {"regex": r"[a-z][\w$]*", "dialects": ["lowercase_english"]},
            {"regex": r"[a-zA-Z][\w$]*"},
        ],
        "hello": [
            {"literal": "hola", "dialects": ["spanish"]},
            {"literal": "salam", "dialects": ["bengali", "arabic"]},
            {"literal": "hello"},
        ],
    }
    assert actual == expected