# Changelog

## Version 0

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
