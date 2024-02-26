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


def test_select_where_union():
    raw_query = """
    its giving a, b, c
    tfw x be 100
    with the bois
    its giving a, b, c
    tfw y be 100
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


def test_select_where_union_all():
    raw_query = """
    its giving a, b, c
    tfw x be 100
    with all the bois
    its giving a, b, c
    tfw y be 100
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


def test_join_two_tables():
    raw_query = """
    its giving a, b
    yass table_a
    come through left table_b
    bet a be b
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT a, b
FROM table_a
LEFT JOIN table_b
ON a = b
;
    """.strip()
    assert actual == expected


def test_join_three_tables():
    raw_query = """
    its giving a, b, c
    yass table_a
    come through left table_b
        bet a be b
    come through full outer table_c
        bet a sike c
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT a, b, c
FROM table_a
LEFT JOIN table_b
ON a = b
FULL OUTER JOIN table_c
ON a != c
;
    """.strip()
    assert actual == expected


def test_join_three_tables_multiple_conditions():
    raw_query = """
    its giving a, b, c
    yass table_a
    come through left table_b
        bet a be b
        fax 1 be 1
        uh b sike "quack"
    come through full outer table_c
        bet a sike c
        fax 1 be 1
        uh c sike "quack"
    no cap
    """
    actual = Zql().parse(raw_query, use_grammar=True)
    expected = """
SELECT a, b, c
FROM table_a
LEFT JOIN table_b
ON a = b
AND 1 = 1
OR b != "quack"
FULL OUTER JOIN table_c
ON a != c
AND 1 = 1
OR c != "quack"
;
    """.strip()
    assert actual == expected
