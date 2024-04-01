NEWLINE = "\n"
SPACE = " "
OPEN_PAREN = "("
CLOSE_PAREN = ")"
SEMICOLON = ";"


def normalize_query(query: str) -> str:
    lines = query.strip().split(NEWLINE)
    normal = SPACE.join([l.strip() for l in lines])
    normal = normal.replace(OPEN_PAREN + SPACE, OPEN_PAREN)
    normal = normal.replace(SPACE + CLOSE_PAREN, CLOSE_PAREN)
    normal = normal.replace(SPACE + SEMICOLON, SEMICOLON)
    normal = normal.strip()
    return normal