import re

from typing import List, Optional


SPACE = " "
COMMENT_CHAR = "-"
MULTI_LINE_COMMENT_START = ["/", "*"]
MULTI_LINE_COMMENT_END = ["*", "/"]
NEWLINE = "\n"
WHITESPACE_REGEX = re.compile(r"\s+")
NEED_SPACE_AROUND_CHARS = [";", ",", ".", "(", ")", "+", "-", "*", "/", "="]
QUOTES = {"\"", "'"}


def get_tokens(source: str) -> List[str]:
    """
    Converts a raw source string to a list of tokens.
    - Strips whitespace from either side.
    - Adds spaces around characters like commas so they become tokens.
    - Ignores extra whitespace or line breaks in the query.
    """
    normalized = source.strip()
    cleaned = WHITESPACE_REGEX.sub(SPACE, normalized)
    for char in NEED_SPACE_AROUND_CHARS:
        cleaned = cleaned.replace(char, SPACE + char + SPACE)
    separated = cleaned.split(SPACE)
    tokens = [t for t in separated if t]
    return tokens


def is_single_line_comment_at(i: int, chars: List[str]) -> bool:
    """Checks if a single line comment starts at position `i` of `chars`."""
    if len(chars) <= i + 1:
        return False
    return chars[i] == COMMENT_CHAR and chars[i + 1] == COMMENT_CHAR


def is_multi_line_comment_at(i: int, chars: List[str]) -> bool:
    """Checks if a multi line comment starts at position `i` of `chars`."""
    if len(chars) <= i + 1:
        return False
    return (
        chars[i] == MULTI_LINE_COMMENT_START[0]
        and chars[i + 1] == MULTI_LINE_COMMENT_START[1]
    )


def is_end_of_multi_line_comment_at(i: int, chars: List[str]) -> bool:
    """Checks if a multi line comment ends at position `i` of `chars`."""
    if len(chars) <= i + 1:
        return False
    return (
        chars[i] == MULTI_LINE_COMMENT_END[0]
        and chars[i + 1] == MULTI_LINE_COMMENT_END[1]
    )


def get_tokens_string_safe(source: str) -> List[str]:
    """
    Converts a raw source string to a list of tokens.
    - Strips whitespace from either side.
    - Ensures that non-whitespace separating characters become single tokens.
    - Creates a single token for a quoted string, even if contains whitespace or
      separating characters.
    - Ignores comments.
    - Ignores other extra whitespace or line breaks in the query.
    """
    chars: str = source.strip()
    # Scan characters to accumulate tokens
    tokens: List[str] = []
    token_chars: List[str] = []
    open_quote: Optional[str] = None
    ignore_next: bool = False
    is_single_line_comment: bool = False
    is_multi_line_comment: bool = False
    for i, c in enumerate(chars):
        if ignore_next:
            ignore_next = False
            pass
        elif is_single_line_comment:
            if c == NEWLINE:
                # Found end of single line comment
                is_single_line_comment = False
            else:
                # Found char in single line comment
                pass
        elif is_multi_line_comment:
            if is_end_of_multi_line_comment_at(i, chars):
                # Found end of multi line comment
                is_multi_line_comment = False
                ignore_next = True
            else:
                # Found char in multi line comment
                pass
        elif open_quote is not None:
            if c == open_quote:
                # Found close quote
                token_chars.append(c)
                token = "".join(token_chars)
                tokens.append(token)
                token_chars = []
                open_quote = None
            else:
                # Found char in quoted string
                token_chars.append(c)
        elif WHITESPACE_REGEX.match(c):
            # Found non-quoted whitespace
            if token_chars:
                token = "".join(token_chars)
                tokens.append(token)
                token_chars = []
        elif is_single_line_comment_at(i, chars):
            # Found start of single line comment
            is_single_line_comment = True
        elif is_multi_line_comment_at(i, chars):
            # Found start of multi line comment
            is_multi_line_comment = True
        elif c in NEED_SPACE_AROUND_CHARS:
            # Found character token
            if token_chars:
                token = "".join(token_chars)
                tokens.append(token)
                token_chars = []
            tokens.append(c)
        elif c in QUOTES:
            # Found open quote
            if token_chars:
                token = "".join(token_chars)
                tokens.append(token)
                token_chars = []
            open_quote = c
            token_chars.append(c)
        else:
            # Found other char
            token_chars.append(c)
    # Capture all remaining accumulated token chars into a token
    if token_chars:
        token = "".join(token_chars)
        tokens.append(token)
        token_chars = []
    return tokens
