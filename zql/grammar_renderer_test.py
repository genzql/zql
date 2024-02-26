import pytest
from zql.grammar import parse_grammar, parse_ast
from zql.grammar_renderer import QueryRenderError, render_query


FUNCTION_GRAMMAR_CONTENT = r"""
    root     : function
             ;
    function : arg1 divide arg2
             > "{arg1}\n---------------------\n{arg2}"
             | arg1 operator arg2
             > "{operator}({arg1}, {arg2})"
             | expr
             ;
    arg1     : expr
             ;
    arg2     : expr
             ;
    expr     : open function close
             > "{function}"
             | word
             | number
             ;
    open     : "("
             ;
    close    : ")"
             ;
    word     : r[a-zA-Z][\w$]*
             ;
    number   : r[0-9]+
             ;
    operator : add
             | subtract
             | multiply
             | divide
             ;
    add      : "+"
             > "add"
             ;
    subtract : "-"
             > "subtract"
             ;
    multiply : "*"
             > "multiply"
             ;
    divide   : "/"
             > "divide"
             ;
"""
FUNCTION_GRAMMAR = parse_grammar(FUNCTION_GRAMMAR_CONTENT)


def test_render_simple():
    ast = parse_ast(FUNCTION_GRAMMAR, "2 + 3")
    actual = render_query(FUNCTION_GRAMMAR, ast)
    assert actual == "add(2, 3)"


def test_render_nested():
    ast = parse_ast(FUNCTION_GRAMMAR, "(2 + 3) - (1000 * K)")
    actual = render_query(FUNCTION_GRAMMAR, ast)
    assert actual == "subtract(add(2, 3), multiply(1000, k))"


def test_render_fancy_case():
    ast = parse_ast(FUNCTION_GRAMMAR, "(2 + 3) / (1000 * K)")
    actual = render_query(FUNCTION_GRAMMAR, ast)
    assert actual == """
add(2, 3)
---------------------
multiply(1000, k)
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
