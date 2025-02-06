from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import  Request 


router = APIRouter()


templates = Jinja2Templates(directory="Frontend/templates")

# Ruta principal
@router.get("/home", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("home.html",{"request": request})

