import sqlite3
from sqlite3 import Cursor

from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates

from zql.main import Zql

templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "main.html", {"request": request, "transpilation_result": "", "client_response": ">"}
    )


@app.post("/transpile")
async def transpile_string(request: Request, inputString: str = Form(...)):
    connection = sqlite3.connect("zql.db")
    db_session = connection.cursor()
    # transpilation logic here
    transpilation_result = Zql().parse(inputString)

    try:
        result = db_session.execute(transpilation_result).fetchall()
        connection.commit()
    except sqlite3.OperationalError as e:
        result = f"Error {e}"



    return templates.TemplateResponse(
        "main.html", {"request": request, "transpilation_result": transpilation_result, "client_response": f"> {result}"}
    )
