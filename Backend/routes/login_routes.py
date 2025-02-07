from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import  Request 


route = APIRouter()


templates = Jinja2Templates(directory="Frontend/templates")

# Ruta principal
@route.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("login.html",{"request": request})