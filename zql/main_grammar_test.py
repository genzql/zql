import pytest
from zql.main import Zql


def test_simple_select_query():
    raw_query = """
    its giving a, b
    yass example
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
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
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT a, b
FROM example
LIMIT 10
;
    """.strip()
    assert actual == expected


def test_select_integer_without_from():
    raw_query = """
    its giving 6
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT 6
;
    """.strip()
    assert actual == expected


def test_select_float_without_from():
    raw_query = """
    its giving 6.04
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT 6.04
;
    """.strip()
    assert actual == expected


def test_select_without_from_string_expression_single_quotes():
    raw_query = """
    its giving 'hello'
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT 'hello'
;
    """.strip()
    assert actual == expected


def test_select_without_from_string_expression_double_quotes():
    raw_query = """
    its giving "hello"
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT "hello"
;
    """.strip()
    assert actual == expected


def test_single_where():
    raw_query = """
    its giving a
    yass example
    tfw a be b
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT a
FROM example
WHERE a = b
;
    """.strip()
    assert actual == expected


def test_multi_where_and():
    raw_query = """
    its giving a
    yass example
    tfw a be b
    fax a sike c
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT a
FROM example
WHERE a = b
AND a != c
;
    """.strip()
    assert actual == expected


def test_multi_where_or():
    raw_query = """
    its giving a
    yass example
    tfw a be b
    uh a sike c
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT a
FROM example
WHERE a = b
OR a != c
;
    """.strip()
    assert actual == expected


def test_multi_where_and_or():
    raw_query = """
    its giving a
    yass example
    tfw a be b
    fax a sike c
    uh b be c
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT a
FROM example
WHERE a = b
AND a != c
OR b = c
;
    """.strip()
    assert actual == expected


def test_single_where_string_expression():
    raw_query = """
    its giving a
    yass example
    tfw a be 'ahh'
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT a
FROM example
WHERE a = 'ahh'
;
    """.strip()
    assert actual == expected


def test_simple_select_union():
    raw_query = """
    its giving a, b, c
    with the bois
    its giving a, b, c
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT a, b, c
UNION
SELECT a, b, c
;
    """.strip()
    assert actual == expected


def test_simple_select_union_all():
    raw_query = """
    its giving a, b, c
    with all the bois
    its giving a, b, c
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT a, b, c
UNION ALL
SELECT a, b, c
;
    """.strip()
    assert actual == expected


# @pytest.mark.skip()
def test_select_where_union():
    raw_query = """
    its giving a, b, c
    twf x be 100
    with the bois
    its giving a, b, c
    twf y be 100
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT a, b, c
WHERE x = 100
UNION
SELECT a, b, c
WHERE y = 100
;
    """.strip()
    assert actual == expected


# @pytest.mark.skip()
def test_select_where_union_all():
    raw_query = """
    its giving a, b, c
    twf x be 100
    with all the bois
    its giving a, b, c
    twf y be 100
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT a, b, c
WHERE x = 100
UNION ALL
SELECT a, b, c
WHERE y = 100
;
    """.strip()
    assert actual == expected
