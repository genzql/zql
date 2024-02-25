import sqlite3
from sqlite3 import Cursor

from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates

from zql import Zql, ZqlParserError


def setup_db(session):
    session.execute("DROP TABLE IF EXISTS apples;")
    session.execute("""
        CREATE TABLE apples(
            owner text,
            num_apples int
        );
    """)
    session.execute("INSERT INTO apples VALUES ('vinesh', 5);")
    session.connection.commit()


templates = Jinja2Templates(directory="templates")

app = FastAPI()

connection = sqlite3.connect("zql.db")
db_session = connection.cursor()
setup_db(db_session)


def get_result_dicts(rows: list[tuple], columns: list[tuple]) -> list[dict]:
    """
    Transforms SQLite rows and columns into dicts with column names as keys and
    column values as values.
    """
    column_names = [col[0] for col in columns]
    results = [dict(zip(column_names, row)) for row in rows]
    return results


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "main.html", {"request": request, "transpilation_result": "", "client_response": ">"}
    )


@app.post("/transpile")
async def transpile_string(request: Request, inputString: str = Form(...)):
    error_message: str | None = None
    transpilation_result: str = ""
    try:
        transpilation_result = Zql().parse(inputString)
    except ZqlParserError as zpe:
        error_message = str(zpe)

    result: list[dict] = []
    if not error_message:
        try:
            cursor = db_session.execute(transpilation_result)
            rows = cursor.fetchall()
            columns = cursor.description
            connection.commit()
            results = get_result_dicts(rows, columns)
        except sqlite3.OperationalError as soe:
            error_message = str(soe)

    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "query": inputString,
            "transpilation_result": transpilation_result,
            "client_response": results,
            "error_message": error_message,
        }
    )
