import re
from zql.types import ZqlQuery, AstNode, Token, NodeType


SPACE = " "
COMMA_WITH_SPACE = " ,"
WHITESPACE_REGEX = re.compile(r"\s+")
COMMA_REGEX = re.compile(r",")


def query_to_tokens(raw: ZqlQuery) -> list[Token]:
    """
    Converts a raw quuery to a list of tokens.
    - Strips whitespace from either side.
    - Converts text to lowercase.
    - Converts Unicode characters to ASCII.
    - Adds spaces before commas so they become tokens.
    - Ignores extra whitespace or line breaks in the query.
    """
    normalized = raw.strip().casefold()
    cleaned = WHITESPACE_REGEX.sub(SPACE, normalized)
    cleaned_with_commas = COMMA_REGEX.sub(COMMA_WITH_SPACE, cleaned)
    separated = cleaned_with_commas.split(SPACE)
    tokens = [t for t in separated if t]
    return tokens


class ZqlParserError(Exception):
    pass


BLANK = ""
COMMA = ","
INT = "int"
EXPR = "expression"
EXPRESSION_LIST = "expression_list"
SELECT_CLAUSE = "select_clause"
FROM_CLAUSE = "from_clause"
WHERE_CLAUSE = "where_clause"
LIMIT_CLAUSE = "limit_clause"
TERMINAL = "terminal"

EXPR_RE = re.compile(r"(\'|\")?[(a-z)|(0-9)]+(\'|\")?")
INT_RE = re.compile(r"[0-9]+")
COMPARISON_TOKEN_MAP = {
    "be": "=",
    "sike": "!="
}
FILTER_OP_TOKEN_MAP = {
    "fax": "AND",
    "uh": "OR"
}
SELECT_CLAUSE_TOKENS = ["its", "giving"]
FROM_CLAUSE_TOKEN = "yass"
WHERE_CLAUSE_TOKEN = "tfw"
LIMIT_CLAUSE_TOKENS = ["say", "less"]
TERMINAL_TOKENS = ["no", "cap"]


def has_tokens_next(tokens: list[Token], expecting: list[Token]) -> bool:
    """
    Checks if the expected tokens are found at the start of the token list.
    """
    n = len(expecting)
    next_tokens = tokens[0:n]
    return next_tokens == expecting


def pop_tokens(tokens: list[Token], n: int):
    """Removes the given number of tokens from the front of the list."""
    for i in range(n):
        tokens.pop(0)


def safe_pop(tokens: list[Token]) -> Token:
    """
    Removes and returns the first token.
    Returns a blank space if the list is empty.
    """
    return tokens.pop(0) if tokens else BLANK


def safe_peek(tokens: list[Token]) -> Token:
    """
    Returns the first token but does not remove it from the list.
    Returns a blank space if the list is empty.
    """
    return tokens[0] if tokens else BLANK


def parse_expression_list(tokens: list[Token]) -> list[AstNode]:
    """
    Parses a list of one or more expression nodes from the token list, while
    modifying the token list.
    """
    nodes: list[AstNode] = []
    while tokens:
        token = safe_pop(tokens)
        if not EXPR_RE.match(token):
            raise ZqlParserError(f"Expected expression, not `{token}`.")

        expr_node = {"type": NodeType.EXPRESSION.value, "value": token}
        nodes.append(expr_node)
        
        next_token = safe_peek(tokens)
        if next_token == COMMA:
            tokens.pop(0)
        else:
            break
    return nodes


def parse_filter(tokens: list[Token]) -> AstNode:
    """
    Parses a single filter node from the token list, while modifying the list.
    """
    token_a = safe_pop(tokens)
    if not EXPR_RE.match(token_a):
        raise ZqlParserError(f"Expected expression, not `{token_a}`.")

    token = safe_pop(tokens)
    comparison = COMPARISON_TOKEN_MAP.get(token)
    if comparison is None:
        raise ZqlParserError(
            f"Expected filter comparison, not `{token}`."
        )

    token_b = safe_pop(tokens)
    if not EXPR_RE.match(token_b):
        raise ZqlParserError(f"Expected expression, not `{token_b}`.")

    filter_node = {
        "type": NodeType.FILTER.value,
        "value": comparison,
        "children": [
            {"type": NodeType.EXPRESSION.value, "value": token_a},
            {"type": NodeType.EXPRESSION.value, "value": token_b},
        ]
    }
    return filter_node


def parse_filter_ast(tokens: list[Token]) -> AstNode:
    """
    Parses an abstract syntax tree of one or more filter nodes from the token
    list, while modifying the token list.
    """
    filter_node_a: AstNode | None = None
    while tokens:
        if filter_node_a is None:
            filter_node_a: AstNode = parse_filter(tokens)

        token = safe_peek(tokens)
        operator = FILTER_OP_TOKEN_MAP.get(token)
        if operator is None:
            filter_ast = {
                "type": NodeType.FILTER_BRANCH.value,
                "value": None,
                "children": [filter_node_a]
            }
            break
        
        token = tokens.pop(0)
        filter_node_b = parse_filter(tokens)
        filter_node = {
            "type": NodeType.FILTER_BRANCH.value,
            "value": operator,
            "children": [filter_node_a, filter_node_b]
        }
        filter_node_a = filter_node

        token = safe_peek(tokens)
        operator = FILTER_OP_TOKEN_MAP.get(token)
        if operator is None:
            break

    return filter_node_a


def parse_to_ast(raw: ZqlQuery) -> AstNode:
    """Converts a raw ZQL query to an abstract syntax tree."""
    tokens = query_to_tokens(raw)

    ast_children: list[AstNode] = []
    expected_tokens = [SELECT_CLAUSE]
    while tokens or expected_tokens:
        expecting = expected_tokens.pop(0)

        if expecting == SELECT_CLAUSE:
            if not has_tokens_next(tokens, SELECT_CLAUSE_TOKENS):
                raise ZqlParserError(
                    f"Expected `its giving`, not `{tokens[0:2]}`."
                )

            pop_tokens(tokens, len(SELECT_CLAUSE_TOKENS))
            expression_nodes = parse_expression_list(tokens)
        
            next_token = safe_peek(tokens)
            if next_token == FROM_CLAUSE_TOKEN:
                expected_tokens.append(FROM_CLAUSE)
            else:
                expected_tokens.append(TERMINAL)

            select_node = {
                "type": NodeType.SELECT.value,
                "children": expression_nodes
            }
            ast_children.append(select_node)
        
        if expecting == FROM_CLAUSE:
            token = safe_pop(tokens)
            if token != FROM_CLAUSE_TOKEN:
                raise ZqlParserError(f"Expected `yass`, not `{token}`.")

            token = safe_pop(tokens)
            if not EXPR_RE.match(token):
                raise ZqlParserError(f"Expected expression, not `{token}`.")

            from_node = {
                "type": NodeType.FROM.value,
                "children": [
                    {"type": "expression", "value": token}
                ]
            }
            ast_children.append(from_node)
            
            next_token = safe_peek(tokens)
            if has_tokens_next(tokens, TERMINAL_TOKENS):
                expected_tokens.append(TERMINAL)
            elif next_token == WHERE_CLAUSE_TOKEN:
                expected_tokens.append(WHERE_CLAUSE)
            else:
                expected_tokens.append(LIMIT_CLAUSE)
        
        if expecting == WHERE_CLAUSE:
            token = safe_pop(tokens)
            if token != WHERE_CLAUSE_TOKEN:
                raise ZqlParserError(
                    f"Expected `tfw`, not `{token}`."
                )

            filter_ast = parse_filter_ast(tokens)
        
            if has_tokens_next(tokens, LIMIT_CLAUSE_TOKENS):
                expected_tokens.append(LIMIT_CLAUSE)
            else:
                expected_tokens.append(TERMINAL)

            where_node = {
                "type": NodeType.WHERE.value,
                "children": [filter_ast]
            }
            ast_children.append(where_node)

        if expecting == LIMIT_CLAUSE:
            if not has_tokens_next(tokens, LIMIT_CLAUSE_TOKENS):
                raise ZqlParserError(
                    f"Expected `say less`, not `{tokens[0:2]}`."
                )
            
            pop_tokens(tokens, len(LIMIT_CLAUSE_TOKENS))

            token = safe_pop(tokens)
            if not INT_RE.match(token):
                raise ZqlParserError(f"Expected integer, not `{token}`.")
            
            expected_tokens.append(TERMINAL)

            limit_node = {
                "type": NodeType.LIMIT.value,
                "children": [
                    {"type": "integer", "value": token}
                ]
            }
            ast_children.append(limit_node)
            
        if expecting == TERMINAL:
            if not has_tokens_next(tokens, TERMINAL_TOKENS):
                raise ZqlParserError(
                    "You're cappin bro. "
                    f"Expected `no cap`, not `{tokens[0:2]}`."
                )
            
            pop_tokens(tokens, len(TERMINAL_TOKENS))

            terminal_node = {"type": NodeType.TERMINAL.value}
            ast_children.append(terminal_node)

    final_ast = {"type": "query", "children": ast_children}
    return final_ast
