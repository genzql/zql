# ZQL Parser

## Scope

### In Scope

- `zql` just parses raw ZQL queries to raw SQLite queries.

### Out of Scope

- Full SQLite functionality. ZQL only supports a subset of SQLite until we have slang for more.
- Outputting to other dialects. Use SQLglot or add new ZQL renderers.
- Templated query variables. Add support in future.

## Architecture

- Parser: Converts raw ZQL string to abstract sytnax tree (AST).
- Renderer: Converts AST to raw SQLite string.
- Helpers: Convenience methods for callers.

## Vision

### Tests For External API

```python
from zql import Zql
from zql.helpers import is_same_query


def test_create_query():
    raw_query = """
    built different girlie example be (
        a valid(varchar),
        b valid(zaddyint)
    )
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
    CREATE TABLE example(a TEXT NOT NULL, b NUMERIC NOT NULL);
    """
    assert is_same_query(actual, expected)

def test_insert_query():
    raw_query = """
    pushin p into example ('A', 1) no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
    INSERT INTO example VALUES ('A', 1);
    """
    assert is_same_query(actual, expected)

def test_select_query():
    raw_query = """
    its giving a, b
    yass example
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
    SELECT a, b FROM example;
    """
    assert is_same_query(actual, expected)
```

### Tests for (Internal) API

See actual tests 😊

## Grammar

See `zql/zql_grammar.tmjd`.
