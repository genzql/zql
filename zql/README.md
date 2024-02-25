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

### Current Grammar

- [x] Simple select queries
- [ ] Simple create queries
- [ ] Simple insert queries
- [ ] Inline comments

```
TERMINAL = (no cap)
EXPR = [(a-z)|(0-9)]+
INT = [0-9]+

COMMA = ,
SELECT = (its giving)
FROM = (yass)
WHERE = (tfw)
LIMIT = (say less)
KEYWORD = SELECT|FROM|WHERE|LIMIT
COMPARISON = be|(sike)
FILTER_OP = fax|uh

QUERY        : SELECT_CLAUSE
             ;
EXPR_LIST    : EXPR
             | EXPR COMMA EXPR_LIST
             ;
SELECT_CLAUSE: EXPR_LIST FROM_CLAUSE
             | EXPR_LIST TERMINAL
             ;
FROM_CLAUSE  : EXPR TERMINAL
             | EXPR WHERE_CLAUSE
             | EXPR LIMIT_CLAUSE
             ;
FILTER       : EXPR COMPARISON EXPR
             ;
FILTER_LIST  : FILTER
             | FILTER FILTER_OP FILTER_LIST
             ;
WHERE_CLAUSE : FILTER_LIST TERMINAL
             | FILTER_LIST LIMIT_CLAUSE
             ;
LIMIT_CLAUSE : INT TERMINAL
             ;
```

### Future Grammar

```
root              : query terminal
                  ;
statement         : query_stmt
                  | definition_stmt
                  | manipulation_stmt
                  ;
query_stmt        : explain query
                  | query
                  ;
query             : cte_clause simple_query
                  | simple_query
                  ;
cte_clause        : "with" cte_list
                  ;
cte_list          : aliased_sub_query comma cte_list
cte_list          | aliased_sub_query
                  ;
aliased_sub_query : sub_query alias word
                  ;
sub_query         : open_paren simple_query close_paren 
                  ;
simple_query      : select_query union_clause select_query
                  | select_query
                  ;
select_query      : select_clause from_query
                  | select_clause
                  ;
from_query        : from_clause where_query
                  | from_clause
                  | where_query
                  ;
where_query       : where_clause groupby_query
                  | where_clause
                  | groupby_query
                  ;
groupby_query     : groupby_clause having_query
                  | groupby_clause
                  | having_query
                  ;
having_query      : having_clause orderby_query
                  | having_clause
                  | orderby_query
                  ;
orderby_query     : orderby_clause limit_clause
                  | orderby_clause
                  | limit_clause
                  ;
select_clause     : select select_expr_list
                  ;
select_expr_list  : select_expr comma select_expr_list
                  | select_expr
                  ;
select_expr       : expression alias word
                  | expression
                  ;
expr_list         : expression comma expr_list
                  | expression
                  ;
expression        : expression operator expression
                  | function_expr
                  | dot_expression
                  | quoted_expr
                  | float
                  | number
                  | word
                  ;
dot_expression    : word dot word
                  ;
operator          : is
                  | is_not
                  | equal
                  | not_equal
                  | math_operator
                  ;
function_expr     : function_name open_paren argument_list close_paren
                  ;
argument_list     : expression comma argument_list
                  | expression
                  ;
from_clause       : from table join_list
                  | from table
                  ;
table             : sub_query alias word
                  | sub_query word
                  | sub_query
                  | table_name
                  ;
table_name        : word alias word
                  | word word
                  | word
                  ;
join_list         : join_clause join_list
                  | join_clause
                  ;
join_clause       : comma table 
                  | join_with_type table join_on condition_list
                  ;
join_with_type    : join join_type
                  | join
                  ;
where_clause      : where condition_list
                  ;
condition_list    : expression cond_operator expression
                  | expression
                  ;
cond_operator     : and
                  | or
                  ;
groupby_clause    : groupby_start expr_list groupby_end
                  ;
having_clause     : having_start condition_list having_end
                  ;
orderby_clause    : orderby orderby_list
                  ;
orderby_list      : orderby_expr comma orderby_expr
                  | orderby_expr
                  ;
orderby_expr      : expression direction
                  ;
direction         : asc
                  | desc
                  | nulls first
                  | nulls last
                  ;
limit_clause      : limit limit_amount
                  ;
limit_amount      : number
                  ;
union_clause      : union all
                  | union
                  ;
definition_stmt   : create_stmt
                  | drop_stmt
                  ;
create_stmt       : create_db_stmt
                  | create_table_stmt
                  ;
create_db_stmt    : create_db if_not_exists word
                  | create_db word
                  ;
create_table_stmt : create_table if_not_exists db_table alias table_definition
                  ;
table_definition  : open_paren column_def_list close_paren
                  ;
column_def_list   : column_def comma column_def_list
                  | column_def
                  ;
column_def        : word column_type_expr
                  ;
column_type_expr  : column_type expr_list
                  | column_type
                  ;
column_type       : function_expr
                  | word
                  ;
drop_stmt         : drop_db_stmt
                  | drop_table_stmt
                  ;
drop_db_stmt      : drop_db word if_exists
                  | drop_db word
                  ;
drop_table_stmt   : drop_table db_table if_exists
                  | drop_table db_table
                  ;
db_table          : word dot word
                  | word
                  ;
manipulation_stmt : insert_stmt
                  ;
insert_stmt       : insert_into db_table open_paren expr_list close_paren
                  ;
select            : "its giving"
                  ;
from              : "yass"
                  ;
join              : "come through"
                  ;
join_on           : "bet"
                  ;
join_type         : "inner"
                  | "left"
                  | "left outer"
                  | "right"
                  | "right outer"
                  | "full outer"
                  | "cross"
                  ;
where             : "tfw"
                  ;
and               : "fax"
                  ;
or                : "uh"
                  ;
groupby_start     : "let"
                  ;
groupby_end       : "cook"
                  ;
having_start      : "catch these"
                  ;
having_end        : "hands"
                  ;
orderby           : "ngl"
                  ;
limit             : "say less"
                  ;
union_all         : "with all the bois"
                  ;
union             : "with the bois"
                  ;
explain           : "whats good with"
                  ;
dot               : "."
                  ;
comma             : ","
                  ;
open_paren        : "("
                  ;
close_paren       : ")"
                  ;
alias             : "be"
                  ;
create_db         : "built different queen"
                  ;
create_table      : "built different girlie"
                  ;
drop_db           : "yeet queen"
                  ;
drop_table        : "yeet girlie"
                  ;
if_not_exists     : "or nah"
                  ;
if_exists         : "or nah"
                  ;
insert_into       : "pushin p into"
                  ;
terminal          : "no cap"
                  ;
```