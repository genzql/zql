import pytest

from typing import List

from zql.genzql.loader import get_zql_grammar
from zql.genzql.translator import translate
from zql.tests.helpers import normalize_query


ZQL_GRAMMAR = get_zql_grammar()


QUERIES: List[str] = [
# Basic data selection from a single table
"""
SELECT name, age FROM users;
""",

# Selection with condition
"""
SELECT name, age FROM users WHERE age > 18;
""",

# Aggregate functions
"""
SELECT AVG(age) AS average_age FROM users;
""",

# Grouping data
"""
SELECT department, COUNT(*) AS number_of_employees FROM employees GROUP BY department;
""",

# Joining tables
"""
SELECT employees.name, departments.name AS department_name
FROM employees
INNER JOIN departments ON employees.department_id = departments.id;
""",

# Subquery in WHERE clause
"""
SELECT name FROM users WHERE age > (SELECT AVG(age) FROM users);
""",

# Using aliases for columns
"""
SELECT name AS employee_name, age AS employee_age FROM employees;
""",

# Inserting data
"""
INSERT INTO users (name, age) VALUES ('John Doe', 28);
""",

# Creating a table
"""
CREATE TABLE departments(
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
""",

# Common Table Expression (CTE)
"""
WITH regional_sales AS (
SELECT region, SUM(amount) AS total_sales
FROM sales
GROUP BY region
)
SELECT region, total_sales
FROM regional_sales
WHERE total_sales > (SELECT AVG(total_sales) FROM regional_sales);
""",

# Using the LIKE operator for pattern matching
"""
SELECT name FROM users WHERE name LIKE '%Doe%';
""",

# Using IN to filter on multiple values
"""
SELECT name, age FROM users WHERE age IN (25, 30, 35);
""",

# Set operations (UNION)
"""
SELECT name FROM employees
UNION
SELECT name FROM contractors;
""",
]


@pytest.mark.parametrize("query", [q.strip() for q in QUERIES])
def test_self_translate_query(query: str):
    zql = translate(ZQL_GRAMMAR, query, source_dialect="sqlite")
    actual = translate(ZQL_GRAMMAR, zql, target_dialect="sqlite")
    assert normalize_query(actual) == normalize_query(query)
