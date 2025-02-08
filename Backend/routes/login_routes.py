from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import  Request 
from fastapi import APIRouter, HTTPException, Depends
from Backend.models import UserCreate, LoginRequest
from Backend.services.auth import create_access_token, get_db, authenticate_user
from Backend.models import User
from sqlalchemy.orm import Session
from fastapi import Form

route = APIRouter()


templates = Jinja2Templates(directory="Frontend/templates")

# Ruta principal
@route.get("/login/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("login.html",{"request": request})

@route.post("/login/")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if not username or not password:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Email y contraseña son requeridos."})

    user = authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Usuario o contraseña incorrectos."})

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token}
