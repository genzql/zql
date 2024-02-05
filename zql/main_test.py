from zql.main import Zql


def test_simple_select_query():
    raw_query = """
    its giving a, b
    yass example
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b
FROM example
;
    """.strip()
    assert actual == expected


def test_simple_select_query_with_limit():
    raw_query = """
    its giving a, b
    yass example
    say less 10
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b
FROM example
LIMIT 10
;
    """.strip()
    assert actual == expected


def test_select_without_from():
    raw_query = """
    its giving 6
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT 6
;
    """.strip()
    assert actual == expected
