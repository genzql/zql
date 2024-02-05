from zql.type_hints import ZqlQuery, SqlQuery


class Zql:
    """Converts ZQL queries to SQL."""

    def __init__(self):
        pass

    def parse(self, raw: ZqlQuery) -> SqlQuery:
        sql = raw.replace("its giving", "select")
        sql = sql.replace(" no cap", ";")
        sql = sql.replace("yass", "from")
        sql = sql.replace("facts", "where")
        sql = sql.replace("yass", "from")
        return sql
