from zql.genzql.cleaner import get_tokens, get_tokens_string_safe


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


def test_get_tokens_string_safe_single_line_comment():
    source = """
    hey
    -- line comment
    lets go -- inline comment
    -- comment with "string" haha
    """
    actual = get_tokens_string_safe(source)
    expected = ["hey", "lets", "go"]
    assert actual == expected


def test_get_tokens_string_safe_multi_line_comment():
    source = """
    hey
    /* block comment
     * hey
     * its over
     */
    lets go -- inline comment
    -- comment with "string" haha
    """
    actual = get_tokens_string_safe(source)
    expected = ["hey", "lets", "go"]
    assert actual == expected


def test_get_tokens_string_safe_end_in_dash():
    source = "yo-"
    actual = get_tokens_string_safe(source)
    expected = ["yo", "-"]
    assert actual == expected


def test_get_tokens_string_safe_multiple_spaces():
    source = "yo    hey"
    actual = get_tokens_string_safe(source)
    expected = ["yo", "hey"]
    assert actual == expected


def test_get_tokens_string_safe_quote_in_word():
    source = "it's me"
    actual = get_tokens_string_safe(source)
    expected = ["it", "'s me"]
    assert actual == expected
