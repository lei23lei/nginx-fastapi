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


@app.get("/client-info")
async def get_client_info(request: Request):
    """Get client connection information"""
    client_host = request.client.host if request.client else "Unknown"
    client_port = request.client.port if request.client else "Unknown"
    
    # Get additional headers that might contain real IP
    forwarded_for = request.headers.get("x-forwarded-for")
    real_ip = request.headers.get("x-real-ip")
    remote_addr = request.headers.get("remote-addr")
    
    return {
        "client_host": client_host,
        "client_port": client_port,
        "remote_addr": remote_addr,
        "x_forwarded_for": forwarded_for,
        "x_real_ip": real_ip,
        "user_agent": request.headers.get("user-agent"),
        "host": request.headers.get("host"),
        "all_headers": dict(request.headers)
    }


@app.get("/remote-info")
async def get_remote_info(request: Request):
    """Get remote connection details"""
    return {
        "remote_host": request.client.host if request.client else None,
        "remote_port": request.client.port if request.client else None,
        "remote_addr": request.client.host if request.client else None,
        "connection_info": {
            "client": str(request.client) if request.client else None,
            "scope": {
                "client": request.scope.get("client"),
                "server": request.scope.get("server"),
                "headers": dict(request.headers)
            }
        }
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
