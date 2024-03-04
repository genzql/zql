import pytest
from zql.parser import parse_ast
from zql.renderer import QueryRenderError, render_query
from zql.sample_grammars import FUNCTION_GRAMMAR, ENGLISH_TRANSLATION_GRAMMAR


def test_render_simple():
    ast = parse_ast(FUNCTION_GRAMMAR, "2 + 3")
    actual = render_query(FUNCTION_GRAMMAR, ast)
    assert actual == "add(2, 3)"


def test_render_nested():
    ast = parse_ast(FUNCTION_GRAMMAR, "(2 + 3) - (1000 * K)")
    actual = render_query(FUNCTION_GRAMMAR, ast)
    assert actual == "subtract(add(2, 3), multiply(1000, K))"


def test_render_fancy_case():
    ast = parse_ast(FUNCTION_GRAMMAR, "(2 + 3) / (1000 * K)")
    actual = render_query(FUNCTION_GRAMMAR, ast)
    assert actual == """
add(2, 3)
---------------------
multiply(1000, K)
    """.strip()


def test_render_grammarless_value_node():
    actual = render_query({}, {"type": "symbol", "value": "X"})
    assert actual == "X"


def test_render_grammarless_child_nodes():
    actual = render_query({}, {
        "type": "series",
        "children": [
            {"type": "symbol", "value": "X"},
            {"type": "symbol", "value": "Y"},
            {"type": "symbol", "value": "Z"},
        ],
    })
    assert actual == "X Y Z"


def test_render_fail_grammarless_no_node_type():
    with pytest.raises(QueryRenderError) as err:
        render_query({}, {"value": "X"})
    actual = str(err.value)
    assert actual == "Node should have a `type`: {'value': 'X'}"


def test_render_fail_grammarless_unable_to_render():
    with pytest.raises(QueryRenderError) as err:
        render_query({}, {"type": "secret"})
    actual = str(err.value)
    assert actual == "Unable to render node: `secret`."


def test_render_fail_no_rule_key():
    with pytest.raises(QueryRenderError) as err:
        grammar_invalid_rule = {
            "start": [{"bogus": "haha", "template": "you'll never find me"}]
        }
        render_query(grammar_invalid_rule, {"type": "start"})
    actual = str(err.value)
    assert actual == "Unable to determine pattern of node: `start`."


def test_render_english_to_spanish():
    actual = render_query(
        ENGLISH_TRANSLATION_GRAMMAR,
        {
            "type": "english",
            "children": [
                {
                    "type": "sentence",
                    "children": [
                        {"type": "hello", "value": "hello"},
                        {"type": "name", "value": "tamjid"},
                    ],
                },
            ],
        },
        target_dialect="spanish"
    )
    assert actual == "hola tamjid"


def test_render_spanish_to_english():
    actual = render_query(ENGLISH_TRANSLATION_GRAMMAR, {
        "type": "english",
        "children": [
            {
                "type": "sentence",
                "children": [
                    {"type": "hello", "value": "hola"},
                    {"type": "name", "value": "tamjid"},
                ],
            },
        ],
    })
    assert actual == "hello tamjid"


def test_render_spanish_to_bengali():
    actual = render_query(
        ENGLISH_TRANSLATION_GRAMMAR,
        {
            "type": "english",
            "children": [
                {
                    "type": "sentence",
                    "children": [
                        {"type": "hello", "value": "hola"},
                        {"type": "name", "value": "tamjid"},
                    ],
                },
            ],
        },
        target_dialect="bengali"
    )
    assert actual == "salam tamjid"