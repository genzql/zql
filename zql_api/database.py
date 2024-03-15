import pandas as pd


TABLES: dict[str, str] = {
    "peeps": "tables/peeps.csv",
    "numbers": "tables/numbers.csv",
}


def setup_db(connection):
    """Loads tables from CSV files with full replacement."""
    for table_name, table_path in TABLES.items():
        df = pd.read_csv(table_path)
        df.to_sql(table_name, connection, if_exists="replace", index=False)
        connection.commit()
