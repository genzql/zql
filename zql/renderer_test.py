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


def test_render_from_ast_where_clause_single_filter():
    ast = {
        "type": "query",
        "children": [
            {
                "type": "select",
                "children": [
                    {"type": "expression", "value": "a"},
                ],
            },
            {
                "type": "from",
                "children": [{"type": "expression", "value": "example"}],
            },
            {
                "type": "where",
                "children": [
                    {
                        "type": "filter",
                        "value": "=",
                        "children": [
                            {"type": "expression", "value": "a"},
                            {"type": "expression", "value": "b"}
                        ]
                    }
                ]
            },
            {"type": "terminal"},
        ]
    }
    actual = render_from_ast(ast)
    expected = """
SELECT a
FROM example
WHERE a = b
;
    """.strip()
    assert actual == expected


def test_render_from_ast_where_clause_multi_filter():
    where_ast = {
        "type": "filter_branch",
        "value": "OR",
        "children": [
            {
                "type": "filter_branch",
                "value": "AND",
                "children": [
                    {
                        "type": "filter",
                        "value": "=",
                        "children": [
                            {"type": "expression", "value": "a"},
                            {"type": "expression", "value": "b"}
                        ]
                    },
                    {
                        "type": "filter",
                        "value": "!=",
                        "children": [
                            {"type": "expression", "value": "a"},
                            {"type": "expression", "value": "c"}
                        ]
                    }
                ]
            },
            {
                "type": "filter",
                "value": "=",
                "children": [
                    {"type": "expression", "value": "b"},
                    {"type": "expression", "value": "c"}
                ]
            }
        ]
    }
    ast = {
        "type": "query",
        "children": [
            {
                "type": "select",
                "children": [
                    {"type": "expression", "value": "a"},
                ],
            },
            {
                "type": "from",
                "children": [{"type": "expression", "value": "example"}],
            },
            {
                "type": "where",
                "children": [where_ast]
            },
            {"type": "terminal"},
        ]
    }
    actual = render_from_ast(ast)
    expected = """
SELECT a
FROM example
WHERE a = b
AND a != c
OR b = c
;
    """.strip()
    assert actual == expected
