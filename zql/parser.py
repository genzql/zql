import re
from zql.type_hints import ZqlQuery, AstNode, Token


SPACE = " "
COMMA_WITH_SPACE = " ,"
WHITESPACE_REGEX = re.compile(r"\s+")
COMMA_REGEX = re.compile(r",")


def query_to_tokens(raw: ZqlQuery) -> list[Token]:
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
LIMIT_CLAUSE = "limit_clause"
TERMINAL = "terminal"

EXPR_RE = re.compile(r"[a-z]+")
INT_RE = re.compile(r"[0-9]+")
SELECT_CLAUSE_TOKENS = ["its", "giving"]
FROM_CLAUSE_TOKEN = "yass"
LIMIT_CLAUSE_TOKENS = ["say", "less"]
TERMINAL_TOKENS = ["no", "cap"]


def has_tokens_next(tokens: list[Token], expecting: list[Token]) -> bool:
    n = len(expecting)
    next_tokens = tokens[0:n]
    return next_tokens == expecting


def pop_tokens(tokens: list[Token], n: int):
    for i in range(n):
        tokens.pop(0)


def safe_pop(tokens: list[Token]) -> Token:
    return tokens.pop(0) if tokens else BLANK


def safe_peek(tokens: list[Token]) -> Token:
    return tokens[0] if tokens else BLANK


def parse_to_ast(raw: ZqlQuery) -> AstNode:
    tokens = query_to_tokens(raw)

    expected_tokens = [SELECT_CLAUSE]
    while tokens or expected_tokens:
        expecting = expected_tokens.pop(0)

        if expecting == SELECT_CLAUSE:
            if not has_tokens_next(tokens, SELECT_CLAUSE_TOKENS):
                raise ZqlParserError(
                    f"Expected `its giving`, not `{tokens[0:2]}`."
                )

            pop_tokens(tokens, len(SELECT_CLAUSE_TOKENS))
            expected_tokens.extend([EXPRESSION_LIST, FROM_CLAUSE])

        if expecting == EXPRESSION_LIST:
            token = safe_pop(tokens)
            if not EXPR_RE.match(token):
                raise ZqlParserError(f"Expected expression, not `{token}`.")
            
            next_token = safe_peek(tokens)
            if next_token == COMMA:
                tokens.pop(0)
                expected_tokens.insert(0, EXPRESSION_LIST)
        
        if expecting == FROM_CLAUSE:
            token = safe_pop(tokens)
            if token != FROM_CLAUSE_TOKEN:
                raise ZqlParserError(f"Expected `yass`, not `{token}`.")

            token = safe_pop(tokens)
            if not EXPR_RE.match(token):
                raise ZqlParserError(f"Expected expression, not `{token}`.")
            
            if has_tokens_next(tokens, TERMINAL_TOKENS):
                expected_tokens.append(TERMINAL)
            else:
                expected_tokens.append(LIMIT_CLAUSE)
        
        if expecting == LIMIT_CLAUSE:
            if not has_tokens_next(tokens, LIMIT_CLAUSE_TOKENS):
                raise ZqlParserError(
                    f"Expected `say less`, not `{tokens[0:2]}`."
                )
            
            pop_tokens(tokens, len(LIMIT_CLAUSE_TOKENS))
            expected_tokens.extend([INT, TERMINAL])

        if expecting == INT:
            token = safe_pop(tokens)
            if not INT_RE.match(token):
                raise ZqlParserError(f"Expected integer, not `{token}`.")
            
        if expecting == TERMINAL:
            if not has_tokens_next(tokens, TERMINAL_TOKENS):
                raise ZqlParserError(
                    "You're cappin bro. "
                    f"Expected `no cap`, not `{tokens[0:2]}`."
                )
            
            pop_tokens(tokens, len(TERMINAL_TOKENS))

    return {}
