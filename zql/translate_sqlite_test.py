from zql.loader import get_zql_grammar
from zql.translator import translate


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