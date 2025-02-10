import bcrypt
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi import  Depends, Form, Request 
from fastapi import APIRouter
from pydantic import EmailStr
from sqlalchemy.orm import Session
from Backend.db.database import get_db
from Backend.models.user_model import UsersRequest


route = APIRouter()


templates = Jinja2Templates(directory="Frontend/templates")

# Ruta principal
@route.get("/login/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("login.html",{"request": request})


@route.post("/login/")
async def login_usuario(
    correo: EmailStr = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(UsersRequest).filter(UsersRequest.correo == correo).first()

    
    if not usuario:
        return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=404)

    if usuario.password != password:  # Asegúrate de verificar con hash si usas bcrypt
        return JSONResponse(content={"error": "Contraseña incorrecta"}, status_code=401)

    return JSONResponse(content={"message": "Inicio de sesión exitoso"}, status_code=200)