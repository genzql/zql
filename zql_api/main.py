import sqlite3
from sqlite3 import Cursor
from pathlib import Path

from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates

from zql_api.database import setup_db
from zql import Zql, ZqlParserError

from fastapi.middleware.cors import CORSMiddleware

TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"

templates = Jinja2Templates(directory=TEMPLATE_DIR)

app = FastAPI()

origins = [
    "http://localhost",
    "https://localhost",
    "http://genzql.com:3000",
    "https://genzql.com",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


connection = sqlite3.connect("zql.db")
db_session = connection.cursor()
setup_db(connection)


def get_result_dicts(rows: list[tuple], column_names: list[str]) -> list[dict]:
    """
    Transforms SQLite rows and columns into dicts with column names as keys and
    column values as values.
    """
    results = [dict(zip(column_names, row)) for row in rows]
    return results

@app.post("/translate")
async def translate_query(source: str, target: str, query: str = Form(...)):
    """Translate to and from ZQL and different SQL dialects."""
    sql: str | None = None
    error: str | None = None
    try:
        sql = Zql().translate(query, source, target)
    except ZqlParserError as zpe:
        error = str(zpe)
    return {"query": sql, "error": error}

@app.post("/run")
async def run_query(query: str = Form(...)) -> dict:
    """Transpile ZQL to SQLite and execute."""
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
            columns = []
            if cursor.description:
                columns = [col[0] for col in cursor.description]
            connection.commit()
            results = get_result_dicts(rows, columns)
        except sqlite3.OperationalError as soe:
            error_message = str(soe)

    return {
        "query": query,
        "transpiled_query": transpiled_query,
        "rows": results,
        "columns": columns,
        "error_message": error_message,
    }


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "main.html", {"request": request}
    )

@app.post("/")
async def run_query(request: Request, query: str = Form(...)):
    """Run ZQL query"""
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
            columns = []
            if cursor.description:
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
