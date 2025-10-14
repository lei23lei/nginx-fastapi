from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static/css", StaticFiles(directory="css"), name="css")
app.mount("/static/images", StaticFiles(directory="images"), name="images")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Welcome to FastAPI",
            "description": "A modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.",
            "message": "Hello! I am FastAPI 🚀"
        }
    )


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
