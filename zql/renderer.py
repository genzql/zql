from zql.types import AstNode, NodeType, SqlQuery


SEMICOLON = ";"


def render_from_ast(ast: AstNode) -> SqlQuery:
    node_type = NodeType(ast.get("type"))
    value = ast.get("value")
    children = ast.get("children", [])

    if node_type == NodeType.QUERY:
        query = "\n".join([render_from_ast(child) for child in children])
        return query
    
    if node_type == NodeType.SELECT:
        columns = ", ".join([render_from_ast(child) for child in children])
        return f"SELECT {columns}"

    if node_type == NodeType.FROM:
        table = children[0].get("value")
        return f"FROM {table}"

    if node_type == NodeType.LIMIT:
        limit = children[0].get("value")
        return f"LIMIT {limit}"

    if node_type == NodeType.EXPRESSION:
        return value

    if node_type == NodeType.INTEGER:
        return value

    if node_type == NodeType.TERMINAL:
        return SEMICOLON

    raise ValueError(f"Unexpected node type: {node_type}")
