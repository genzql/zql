from zql.renderer import render_from_ast


def test_render_from_ast_simple_select():
    ast = {
        "type": "query",
        "children": [
            {
                "type": "select",
                "children": [
                    { "type": "expression", "value": "a" },
                    { "type": "expression", "value": "b" }
                ]
            },
            {
                "type": "from",
                "children": [
                    { "type": "expression", "value": "example" }
                ]
            },
            {"type": "terminal"},
        ]
    }
    actual = render_from_ast(ast)
    expected = """
SELECT a, b
FROM example
;
    """.strip()
    assert actual == expected


def test_render_from_ast_simple_select_with_limit():
    ast = {
        "type": "query",
        "children": [
            {
                "type": "select",
                "children": [
                    { "type": "expression", "value": "a" },
                    { "type": "expression", "value": "b" }
                ]
            },
            {
                "type": "from",
                "children": [
                    { "type": "expression", "value": "example" }
                ]
            },
            {
                "type": "limit",
                "children": [
                    { "type": "integer", "value": "10" }
                ]
            },
            {"type": "terminal"},
        ]
    }
    actual = render_from_ast(ast)
    expected = """
SELECT a, b
FROM example
LIMIT 10
;
    """.strip()
    assert actual == expected
