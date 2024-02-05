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
    LIMIT = "limit"
    EXPRESSION = "expression"
    INTEGER = "integer"
    TERMINAL = "terminal"
