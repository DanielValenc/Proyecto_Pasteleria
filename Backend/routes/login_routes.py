import bcrypt
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import  Depends, HTTPException, Request 
from fastapi import APIRouter
from sqlalchemy.orm import Session
from Backend.db.database import get_db
from Backend.models.user_model import UsersRequest
from Backend.schemas.schema_user import LoginRequest

route = APIRouter()


templates = Jinja2Templates(directory="Frontend/templates")

# Ruta principal
@route.get("/login/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("login.html",{"request": request})


@route.post("/login/")
async def login_usuario(
    user: LoginRequest,
    db: Session = Depends(get_db)
):
    usuario = db.query(UsersRequest).filter(UsersRequest.correo == user.correo).first()

    if usuario and usuario.password == user.password:  # Aquí puedes verificar también el hash de la contraseña
        return {"mensaje": "Inicio de sesión exitoso"}
    else:
        return {"error": "Credenciales incorrectas"}