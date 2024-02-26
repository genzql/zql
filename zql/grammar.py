import re


DEF = ":"
CASE = "|"
TEMPLATE = ">"
END = ";"
REGEX_START = "r"
QUOTE = "\""
SPACE = " "
NEWLINE = "\n"
ESCAPED_NEWLINE = "\\n"
ROOT = "root"


Grammar = dict[str, list[dict]]


class GrammarParseError(Exception):
    pass


def parse_rule(rule: str) -> dict:
    if rule.startswith(REGEX_START):
        regex = rule[1:]
        return {"regex": regex}
    if rule.startswith(QUOTE):
        literal = rule[1:-1]
        return {"literal": literal}
    nodes = rule.split(SPACE)
    return {"sequence": nodes}


def parse_grammar(content: str) -> Grammar:
    raw_lines = [l.strip() for l in content.split("\n")]

    current_node = None
    grammar = {}
    for i, raw_line in enumerate(raw_lines):
        n = i + 1
        line = raw_line.strip()
        if not line:
            continue

        if line == END:
            current_node = None
            continue

        if not current_node:
            def_index = line.find(DEF)
            if def_index < 0:
                raise GrammarParseError(f"L{n}: Missing definition `:`.")

            node = line[:def_index].strip()
            if node in grammar:
                raise GrammarParseError(f"L{n}: Repeat definition of `{node}`.")

            grammar[node] = []
            current_node = node

            raw_rule = line[def_index+1:].strip()
            if not raw_rule:
                raise GrammarParseError(f"L{n}: Missing rule after `:`.")

            rule = parse_rule(raw_rule)
            grammar[current_node].append(rule)
            continue

        template_index = line.find(TEMPLATE)
        case_index = line.find(CASE)

        has_template = template_index > -1
        has_case = case_index > -1
        has_template_first = template_index < case_index
        is_template = has_template and (not has_case or has_template_first)
        if is_template:
            raw_template = line[template_index+1:].strip()
            if not raw_template:
                raise GrammarParseError(f"L{n}: Missing template after `>`.")

            template_no_quotes = raw_template[1:-1]
            template = template_no_quotes.replace(ESCAPED_NEWLINE, NEWLINE)
            current_rules = grammar[current_node]
            if not current_rules:
                raise GrammarParseError(
                    f"L{n}: Missing rule for template on lines above `>`."
                )

            last_rule = current_rules[-1]
            if "template" in last_rule:
                raise GrammarParseError(f"L{n}: Repeat template for rule.")

            last_rule["template"] = template
            continue

        if case_index < 0:
            raise GrammarParseError(f"L{n}: Missing case `|`.")

        raw_rule = line[case_index+1:].strip()
        if not raw_rule:
            raise GrammarParseError(f"L{n}: Missing rule after `|`.")

        rule = parse_rule(raw_rule)
        grammar[current_node].append(rule)

    if current_node:
        raise GrammarParseError("Missing `;` to end grammar.")

    if ROOT not in grammar:
        raise GrammarParseError("Missing `root` definition.")

    return grammar


WHITESPACE_REGEX = re.compile(r"\s+")
NEED_SPACE_AROUND_CHARS = [",", ".", "(", ")"]


AstNode = dict


class AstParseError(Exception):
    pass


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


class TokensManager:

    def __init__(self, tokens: list[str]):
        self.tokens = tokens

    def set_tokens(self, tokens: list[str]):
        self.tokens = tokens

    def copy(self):
        return TokensManager(list(self.tokens))


def evaluate_literal(tokens: list[str], literal: str) -> AstNode:
    tokens_in_literal = len(literal.split(SPACE))
    peeked_tokens = SPACE.join(tokens[:tokens_in_literal]).casefold()
    if peeked_tokens != literal:
        raise AstParseError(f"Expected `{literal}`. Got `{peeked_tokens}`.")
    
    for _ in range(tokens_in_literal):
        tokens.pop(0)
    return {"value": literal}


def evaluate_regex(tokens: list[str], regex: str) -> AstNode:
    if not tokens:
        raise AstParseError(f"Expected match for `{regex}`, not end of input.")

    next_token = tokens[0]
    if not re.compile(regex).match(next_token):
        raise AstParseError(f"Expected `{next_token}` to match `{regex}`.")

    tokens.pop(0)
    return {"value": next_token}


def evaluate_sequence(
    grammar: Grammar,
    tokens_manager: TokensManager,
    sequence: list[str]
) -> AstNode:
    mutable_tokens_manager = tokens_manager.copy()
    children: list[AstNode] = []
    for node in sequence:
        ast_node = evaluate_node(grammar, mutable_tokens_manager, node)
        children.append(ast_node)

    tokens_manager.set_tokens(mutable_tokens_manager.tokens)
    return {"children": children}


def evaluate_rule(
    grammar: Grammar,
    tokens_manager: TokensManager,
    rule: dict
) -> AstNode:
    tokens = tokens_manager.tokens
    literal = rule.get("literal")
    if literal is not None:
        ast_node = evaluate_literal(tokens, literal)
        return ast_node
    
    regex = rule.get("regex")
    if regex is not None:
        ast_node = evaluate_regex(tokens, regex)
        return ast_node
    
    sequence = rule.get("sequence")
    if sequence is not None:
        mutable_tokens_manager = tokens_manager.copy()
        ast_node = evaluate_sequence(grammar, mutable_tokens_manager, sequence)
        mutated_tokens = mutable_tokens_manager.tokens
        tokens_manager.set_tokens(mutated_tokens)
        return ast_node

    raise AstParseError(f"Invalid rule: {rule}")


def evaluate_node(
    grammar: Grammar,
    tokens_manager: TokensManager,
    node: str
) -> AstNode:
    rules = grammar.get(node, [])
    if not rules:
        raise AstParseError(
            f"Reached node `{node}`, which has no defined rules."
        )

    error = None
    ast_node = None
    for rule in rules:
        try:
            mutable_tokens_manager = tokens_manager.copy()
            ast_node = evaluate_rule(grammar, mutable_tokens_manager, rule)
            tokens_manager.set_tokens(mutable_tokens_manager.tokens)
            break
        except Exception as e:
            error = e
            continue

    if not ast_node:
        if error:
            raise error

        remaining_source_sample = SPACE.join(tokens[:3])[:20]
        raise AstParseError(
            f"Failed to parse `{current_node}` at: "
            f"`{remaining_source_sample}`."
        )

    ast_node = {"type": node, **ast_node}
    return ast_node


def parse_ast(grammar: Grammar, source: str) -> AstNode:
    tokens = get_tokens(source)
    tokens_manager = TokensManager(tokens)
    root = evaluate_node(grammar, tokens_manager, ROOT)

    remaining_tokens = tokens_manager.tokens
    if remaining_tokens:
        raise AstParseError(
            "Satisfied `root` rule, but unparsed tokens remain: "
            f"{remaining_tokens}"
        )

    children = root.get("children")
    if not children:
        raise AstParseError("Did not parse anything for `root`.")

    n = len(children)
    if n > 1:
        raise AstParseError(f"Parsed {n} nodes for `root`. Expected only one.")

    return children[0]
