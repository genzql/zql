from enum import Enum
from typing import Dict


ZqlQuery = str
SqlQuery = str
AstNode = Dict
Token = str


class NodeType(Enum):
    QUERY = "query"
    SELECT = "select"
    FROM = "from"
    WHERE = "where"
    LIMIT = "limit"
    FILTER = "filter"
    FILTER_BRANCH = "filter_branch"
    EXPRESSION = "expression"
    INTEGER = "integer"
    TERMINAL = "terminal"
