import pytest

from zql.main import Zql


zql_queries_expectations = [
    ("its giving num_apples yass apples no cap", [(5,)]),
    ("its giving 1 no cap", [(1,)]),
    ("its giving num_apples yass apples tfw owner be 'Vinesh' no cap", [(5,)]),
]


@pytest.mark.usefixtures("setup_db")
@pytest.mark.parametrize("zql_query,expected", zql_queries_expectations)
def test_transpile(session, zql_query, expected):
    transpiled_query = Zql().parse(zql_query)
    result = session.execute(transpiled_query).fetchall()
    assert result == expected
