import pytest

queries = [
    ("SELECT num_apples FROM apples WHERE owner='Vinesh'", [(5,)])
]


@pytest.mark.usefixtures("setup_db")
@pytest.mark.parametrize("query,expected", queries)
def test_query(session, query, expected):
    result = session.execute(query).fetchall()
    assert result == expected
