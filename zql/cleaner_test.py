from zql.cleaner import get_tokens, get_tokens_string_safe


def test_get_tokens():
    source = """
    (A + 12) - 0
    """
    actual = get_tokens(source)
    expected = ["(", "A", "+", "12", ")", "-", "0"]
    assert actual == expected


def test_get_tokens_string_safe():
    source = """
    (A + 12) - 0
    """
    actual = get_tokens_string_safe(source)
    expected = ["(", "A", "+", "12", ")", "-", "0"]
    assert actual == expected


def test_get_tokens_string_safe_quoted_content_no_space():
    source = "get \"red\" from 'colors'"
    actual = get_tokens_string_safe(source)
    expected = ["get", "\"red\"", "from", "'colors'"]
    assert actual == expected


def test_get_tokens_string_safe_quoted_content_space():
    source = "get \"bright red\" from 'cool colors'"
    actual = get_tokens_string_safe(source)
    expected = ["get", "\"bright red\"", "from", "'cool colors'"]
    assert actual == expected


def test_get_tokens_string_safe_quoted_content_inner_quote():
    source = "get \"bright 'big' red\" color"
    actual = get_tokens_string_safe(source)
    expected = ["get", '\"bright \'big\' red\"', "color"]
    assert actual == expected


def test_get_tokens_string_safe_separating_characters():
    source = "get secure.latest when 1+1=2"
    actual = get_tokens_string_safe(source)
    expected = ["get", "secure", ".", "latest", "when", "1", "+", "1", "=", "2"]
    assert actual == expected
