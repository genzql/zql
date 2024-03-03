import re


SPACE = " "
WHITESPACE_REGEX = re.compile(r"\s+")
NEED_SPACE_AROUND_CHARS = [",", ".", "(", ")", "+", "-", "*", "/", "="]
QUOTES = {"\"", "'"}


def get_tokens(source: str) -> list[str]:
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


def get_tokens_string_safe(source: str) -> list[str]:
    """
    Converts a raw source string to a list of tokens.
    - Strips whitespace from either side.
    - Ensures that non-whitespace separating characters become single tokens.
    - Creates a single token for a quoted string, even if contains whitespace or
      separating characters.
    - Ignore other extra whitespace or line breaks in the query.
    """
    # Add a space to the end to ensure the last token gets created
    chars: str = source.strip() + SPACE
    # Scan characters to accumulate tokens
    tokens: list[str] = []
    open_quote: str | None = None
    token_chars: list[str] = []
    for c in chars:
        if open_quote is not None:
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
        elif c in NEED_SPACE_AROUND_CHARS:
            # Found character token
            if token_chars:
                token = "".join(token_chars)
                tokens.append(token)
                token_chars = []
            tokens.append(c)
        elif c in QUOTES:
            # Found open quote
            open_quote = c
            token_chars = [c]
        else:
            # Found other char
            token_chars.append(c)
    return tokens
