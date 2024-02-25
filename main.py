import sqlite3
from sqlite3 import Cursor

from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates

from zql import Zql, ZqlParserError


def setup_db(session):
    session.execute("DROP TABLE IF EXISTS peeps;")
    session.execute("""
        CREATE TABLE peeps(
            name text,
            fave_color text,
            followers int,
            dank float
        );
    """)
    session.execute("INSERT INTO peeps VALUES ('andrew', 'blue', 1700, 0.6);")
    session.execute("INSERT INTO peeps VALUES ('bella', 'green', 1000, 0.4);")
    session.execute("INSERT INTO peeps VALUES ('hugo', 'red', 1400, 0.5);")
    session.execute("INSERT INTO peeps VALUES ('vinesh', 'green', 2700, 0.9);")
    session.execute("INSERT INTO peeps VALUES ('tamjid', '?', 1100, 0.9);")
    session.execute("INSERT INTO peeps VALUES ('laura', '?', 1500, 0.5);")
    session.execute("INSERT INTO peeps VALUES ('nancy', '?', 23, 0.1);")
    session.execute("INSERT INTO peeps VALUES ('lauren', '?', 15, 0.9);")
    session.execute("INSERT INTO peeps VALUES ('david', 'black', 29, 0.7);")
    session.execute("INSERT INTO peeps VALUES ('anshul', 'burgundy', 20, 0.9);")
    session.execute("INSERT INTO peeps VALUES ('steph', 'purple', 41, 0.2);")
    session.execute("INSERT INTO peeps VALUES ('stacy', 'yellow', 20, 0.3);")
    session.connection.commit()


templates = Jinja2Templates(directory="templates")

app = FastAPI()

connection = sqlite3.connect("zql.db")
db_session = connection.cursor()
setup_db(db_session)


def get_result_dicts(rows: list[tuple], column_names: list[str]) -> list[dict]:
    """
    Transforms SQLite rows and columns into dicts with column names as keys and
    column values as values.
    """
    results = [dict(zip(column_names, row)) for row in rows]
    return results


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "main.html", {"request": request, "transpilation_result": "", "client_response": ">"}
    )


@app.post("/transpile")
async def transpile_string(request: Request, query: str = Form(...)):
    error_message: str | None = None
    transpiled_query: str = ""
    try:
        transpiled_query = Zql().parse(query)
    except ZqlParserError as zpe:
        error_message = str(zpe)

    columns: list[str] = []
    results: list[dict] = []
    if not error_message:
        try:
            cursor = db_session.execute(transpiled_query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            connection.commit()
            results = get_result_dicts(rows, columns)
        except sqlite3.OperationalError as soe:
            error_message = str(soe)

    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "query": query,
            "transpiled_query": transpiled_query,
            "rows": results,
            "columns": columns,
            "error_message": error_message,
        }
    )
