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