from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "main.html", {"request": request, "transpilation_result": ""}
    )


@app.post("/transpile")
async def transpile_string(request: Request, inputString: str = Form(...)):
    # transpilation logic here
    transpilation_result = inputString.upper()

    return templates.TemplateResponse(
        "main.html", {"request": request, "transpilation_result": transpilation_result}
    )
