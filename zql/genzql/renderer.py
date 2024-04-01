from typing import Dict, List, Optional, Tuple

from .grammar import Grammar, is_relevant_to_dialect
from .parser import AstNode
from .types import SqlQuery, MaybeDialect


RuleKey = Tuple[str, List[str]]
Template = str
TemplateLookup = Dict[RuleKey, Template]


SPACE = " "
SEQUENCE_RULE_TYPE = "sequence"
NON_CHILDREN_RULE_TYPES = {"literal", "regex"}


class QueryRenderError(Exception):
    pass


def render_query(
    grammar: Grammar,
    ast: AstNode,
    target_dialect: MaybeDialect = None
) -> SqlQuery:
    template_lookup = get_template_lookup(grammar, target_dialect)
    return render_with_grammar(grammar, template_lookup, ast)


def render_with_grammar(
    grammar: Grammar,
    lookup: TemplateLookup,
    ast: AstNode
) -> SqlQuery:
    node_type = ast.get("type")
    children = ast.get("children", [])
    if not node_type:
        raise QueryRenderError(f"Node should have a `type`: {ast}")

    template = maybe_get_template(lookup, ast)
    if template:
        kwargs = {
            c.get("type"): render_with_grammar(grammar, lookup, c)
            for c in children
        }
        rendered = template.format(**kwargs)
        return rendered

    if children:
        args = [render_with_grammar(grammar, lookup, c) for c in children]
        rendered = SPACE.join(args)
        return rendered

    value = ast.get("value")
    if value is not None:
        return value

    raise QueryRenderError(f"Unable to render node: `{node_type}`.")


def maybe_get_template_for_dialect(
    rule: dict,
    target_dialect: MaybeDialect
) -> Optional[str]:
    templates: List[dict] = rule.get("templates")
    if templates is None:
        return None
    
    for template in templates:
        if is_relevant_to_dialect(template, target_dialect):
            return template.get("template")

    return None
    

def get_template_lookup(
    grammar: Grammar,
    target_dialect: MaybeDialect
) -> TemplateLookup:
    template_lookup: TemplateLookup = {}
    for node, rules in grammar.items():
        for rule in rules:
            template = maybe_get_template_for_dialect(rule, target_dialect)
            rule_dialects: List[str] = rule.get("dialects", [])
            literal = rule.get("literal")
            sequence = rule.get("sequence")

            implicit_template = None
            if literal:
                implicit_template = literal
            if sequence:
                nodes = ["{" + name + "}" for name in sequence]
                implicit_template = SPACE.join(nodes)

            no_template = template is None and implicit_template is not None
            if no_template and is_relevant_to_dialect(rule, target_dialect):
                template = implicit_template

            if template is None:
                continue

            key = get_rule_key(node, rule)
            if key in template_lookup:
                break

            template_lookup[key] = template

    return template_lookup


def get_rule_key(node: str, rule: dict) -> RuleKey:
    if SEQUENCE_RULE_TYPE in rule:
        sequence = rule.get(SEQUENCE_RULE_TYPE)
        key = SPACE.join([node, *sequence])
        return key

    for rule_type in NON_CHILDREN_RULE_TYPES:
        if rule_type in rule:
            key = SPACE.join([node, rule_type])
            return key

    raise QueryRenderError(f"Unable to determine pattern of node: `{node}`.")


def maybe_get_template(
    lookup: TemplateLookup,
    ast: AstNode
) -> Optional[Template]:
    node = ast.get("type")
    children = ast.get("children", [])

    if children:
        rule_pattern = [child.get("type") for child in children]
        key = SPACE.join([node, *rule_pattern])
        template = lookup.get(key)
        return template

    for rule_type in NON_CHILDREN_RULE_TYPES:
        key = SPACE.join([node, rule_type])
        template = lookup.get(key)
        if template is not None:
            return template

    return None
