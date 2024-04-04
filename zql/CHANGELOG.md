# Changelog

## Version 0

### 0.3.1

Now supports additional language features:

- `INTERSECTS` (`with the same bois`)
- `CAST(x AS type)` (`trust(x be type)`)
- Fix join type rule order so that outer joins of different types can be parsed
- Allow functions to take star `*` (`sheesh`) as their sole argument
- Allow aliases to be quoted names
- Allow table names to be dotted expressions
- Allow dotted expressions to contain quoted names
- Allow dotted expressions to have as many dot references as needed
- Allow table names in data definition and data manipulation statements to have as many dot references as needed

### 0.3.0

Introduces a breaking change:

- `NOT NULL` is now `is valid` instead of `no yikes`

And supports additional language features:

- `PRAGMA table_info(...)` to describe table schemas (`rizz ...`)
- Support multiple `WHEN ... THEN ...` clauses in `CASE` statements
- Support cool zql data types:
    - `BIGINT` --> `zaddyint`
    - `MEDIUMINT` --> jk we couldn't think of anything for this one so its the same
    - `SMALLINT` --> `smolint`
    - `TINYINT` --> `smolestint`
    - `BOOLEAN` --> `bool`
- Cosmetic: Show each expression on a new line for:
    - `SELECT` expressions
    - `JOIN` conditions
    - `GROUP BY` expressions
    - `HAVING` expressions
- Cosmetic: Show each `WHEN`, `THEN`, `ELSE` expression on a new line in `CASE` statements

### 0.2.1

Now supports additional language features:

- `CASE WHEN ... THEN ... (ELSE ...) END`
    - (`suppose you have ... you finna ... (no worries ...) its chill`)
- `BETWEEN` (`tween`)
- `NULL` (`yikes`)
- `PRIMARY KEY` (`is prime`)
- `NOT NULL` (`no yikes`)
- `==` (`really be`)
- Common table expression formula expresions without parentheses
    - (`WITH 2 + 2 AS four ...`)
- Fix parsing of `IS NOT`

### 0.2.0

Now supports Python >3.5. Also includes additional language features:

- `ARRAY JOIN` (`come through array`)
- `OFFSET` (`after`)
- Join clauses without conditions
- Common table expressions within other common table expressions
- Functions with no arguments
- Math operations on function outputs in the same expression
- Multiple operations in the same expression without parentheses
- Sets with square brackets
- Conversion to and from zql postfix functions (`SUM(x)` <--> `x af`)

### 0.1.1

Initial release. Only supports Python >3.12.

### 0.1.0

Invalid release. Do not use.
