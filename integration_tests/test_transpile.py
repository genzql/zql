import pytest

from zql.main import Zql


zql_queries_expectations = [
    ("its giving num_apples yass apples no cap", [(5,)]),
    ("its giving 1 no cap", [(1,)]),
    ("its giving num_apples yass apples tfw owner be 'vinesh' no cap", [(5,)]),
]


@pytest.mark.usefixtures("setup_db")
@pytest.mark.parametrize("use_grammar", [False, True])
@pytest.mark.parametrize("zql_query,expected", zql_queries_expectations)
def test_transpile(session, zql_query, expected, use_grammar):
    transpiled_query = Zql().parse(zql_query, use_grammar)
    result = session.execute(transpiled_query).fetchall()
    assert result == expected
