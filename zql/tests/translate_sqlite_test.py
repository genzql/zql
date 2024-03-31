from zql.genzql.loader import get_zql_grammar
from zql.genzql.translator import translate


ZQL_GRAMMAR = get_zql_grammar()


def test_simple_select_query():
    raw_query = """
SELECT a, b
FROM example
;
    """
    actual = translate(ZQL_GRAMMAR, raw_query, source_dialect="sqlite")
    expected = """
its giving a, b
yass example
no cap
    """.strip()
    assert actual == expected


def test_simple_select_query_lowercase_single_line():
    raw_query = "select a, b from example;"
    actual = translate(ZQL_GRAMMAR, raw_query, source_dialect="sqlite")
    expected = """
its giving a, b
yass example
no cap
    """.strip()
    assert actual == expected


def test_select_star_query():
    raw_query = """
SELECT *
FROM example
;
    """
    actual = translate(ZQL_GRAMMAR, raw_query, source_dialect="sqlite")
    expected = """
its giving sheesh
yass example
no cap
    """.strip()
    assert actual == expected


def test_groupby_having_with_multiple_fields_and_sort():
    raw_query = """
SELECT a, count(b)
FROM example
GROUP BY a
HAVING count(b) > 10
AND count(b) <= 100
ORDER BY count(b) DESC
;
    """
    actual = translate(ZQL_GRAMMAR, raw_query, source_dialect="sqlite")
    expected = """
its giving a, count(b)
yass example
let a cook
catch these count(b) bops 10
fax count(b) kinda flops 100 hands
ngl count(b) high key
no cap
    """.strip()
    assert actual == expected


def test_join_left():
    raw_query = """
SELECT a, b
FROM table_a
LEFT JOIN table_b
ON c = d
;
    """
    actual = translate(ZQL_GRAMMAR, raw_query, source_dialect="sqlite")
    expected = """
its giving a, b
yass table_a
come through left table_b
bet c be d
no cap
    """.strip()
    assert actual == expected


def test_postfix_aggregation():
    raw_query = """
SELECT a, SUM(b)
FROM example
;
    """
    actual = translate(ZQL_GRAMMAR, raw_query, source_dialect="sqlite")
    expected = """
its giving a, b af
yass example
no cap
    """.strip()
    assert actual == expected


def test_postfix_aggregation_with_alias():
    raw_query = """
SELECT a, SUM(b) AS total
FROM example
;
    """
    actual = translate(ZQL_GRAMMAR, raw_query, source_dialect="sqlite")
    expected = """
its giving a, b af be total
yass example
no cap
    """.strip()
    assert actual == expected


def test_nested_function():
    raw_query = """
SELECT a, COUNT(IF(b, 1, 0)) AS total
FROM example
;
    """
    actual = translate(ZQL_GRAMMAR, raw_query, source_dialect="sqlite")
    expected = """
its giving a, COUNT(IF(b, 1, 0)) be total
yass example
no cap
    """.strip()
    assert actual == expected


def test_nested_sum():
    raw_query = """
SELECT a, COUNT(IF(b, SUM(c), 0)) AS total
FROM example
;
    """
    actual = translate(ZQL_GRAMMAR, raw_query, source_dialect="sqlite")
    expected = """
its giving a, COUNT(IF(b, c af, 0)) be total
yass example
no cap
    """.strip()
    assert actual == expected


def test_count_distinct():
    raw_query = """
SELECT a, COUNT(DISTINCT b) AS unique_b
FROM example
;
    """
    actual = translate(ZQL_GRAMMAR, raw_query, source_dialect="sqlite")
    expected = """
its giving a, COUNT(real ones b) be unique_b
yass example
no cap
    """.strip()
    assert actual == expected


def test_cte_sub_query():
    raw_query = """
WITH table AS (
    SELECT a, b, c
    FROM example
)
SELECT c, b, a
FROM table
;
    """
    actual = translate(ZQL_GRAMMAR, raw_query, source_dialect="sqlite")
    expected = """
perchance table be (
its giving a, b, c
yass example
)
its giving c, b, a
yass table
no cap
    """.strip()
    assert actual == expected


def test_cte_sub_expression():
    raw_query = """
WITH (COUNT(DISTINCT b)) AS unique_count
SELECT a, unique_count
FROM example
;
    """
    actual = translate(ZQL_GRAMMAR, raw_query, source_dialect="sqlite")
    expected = """
perchance (COUNT(real ones b)) be unique_count
its giving a, unique_count
yass example
no cap
    """.strip()
    assert actual == expected


def test_translate_to_self_groupby_having_with_multiple_fields_and_sort():
    original_query = """
SELECT a, count(b)
FROM example
GROUP BY a
HAVING count(b) > 10
AND count(b) <= 100
ORDER BY count(b) DESC
;
    """.strip()
    zql = translate(ZQL_GRAMMAR, original_query, source_dialect="sqlite")
    actual = translate(ZQL_GRAMMAR, zql, target_dialect="sqlite")
    assert actual == original_query