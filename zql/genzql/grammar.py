import re

from typing import Dict, List

from .types import MaybeDialect


DEF = ":"
CASE = "|"
TEMPLATE = ">"
DIALECT = "<"
END = ";"
REGEX_START = "@r"
QUOTE = "\""
SPACE = " "
COMMA = ","
NEWLINE = "\n"
ESCAPED_NEWLINE = "\\n"
TEMPLATES_KEY = "templates"
ROOT = "root"


Grammar = Dict[str, List[dict]]


class GrammarParseError(Exception):
    pass


def parse_rule(rule: str) -> dict:
    is_template = rule.startswith(TEMPLATE)
    is_regex_rule = rule.startswith(REGEX_START)
    is_literal_rule = rule.startswith(QUOTE)

    dialect_index = rule.rfind(DIALECT)
    close_quote_index = rule.rfind(QUOTE)

    has_no_dialect_symbol = dialect_index < 0
    has_dialect_symbol_in_quotes = (
        (is_literal_rule or is_template)
        and close_quote_index > dialect_index
    )
    has_dialects = (
        not has_no_dialect_symbol
        and not has_dialect_symbol_in_quotes
    )

    dialects: List[str] = []
    rule_content = rule
    if has_dialects:
        raw_dialects = rule[dialect_index + 2:]
        dialects = [d.strip() for d in raw_dialects.split(COMMA)]
        rule_content = rule[:dialect_index - 1]


    parsed_rule: dict = {}
    if is_regex_rule:
        regex = rule_content[2:]
        parsed_rule["regex"] = regex
    elif is_literal_rule:
        literal = rule_content[1:-1]
        parsed_rule["literal"] = literal
    elif is_template:
        template_no_quotes = rule_content[3:-1]
        template = template_no_quotes.replace(ESCAPED_NEWLINE, NEWLINE)
        parsed_rule["template"] = template
    else:
        nodes = rule_content.split(SPACE)
        parsed_rule["sequence"] = nodes

    if dialects:
        parsed_rule["dialects"] = dialects

    return parsed_rule


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
            raw_template = line[template_index:].strip()
            if not raw_template:
                raise GrammarParseError(f"L{n}: Missing template after `>`.")

            template = parse_rule(raw_template)
            current_rules = grammar[current_node]
            if not current_rules:
                raise GrammarParseError(
                    f"L{n}: Missing rule for template on lines above `>`."
                )

            last_rule = current_rules[-1]
            if TEMPLATES_KEY not in last_rule:
                last_rule[TEMPLATES_KEY] = []

            last_rule[TEMPLATES_KEY].append(template)
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


def is_relevant_to_dialect(obj: dict, dialect: MaybeDialect) -> bool:
    obj_dialects: List[str] = obj.get("dialects", [])
    is_default_dialect = dialect is None and not obj_dialects
    has_dialect = dialect is not None and dialect in obj_dialects
    supports_any_dialect = not obj_dialects
    is_relevant = (
        is_default_dialect
        or has_dialect
        or supports_any_dialect
    )
    return is_relevant