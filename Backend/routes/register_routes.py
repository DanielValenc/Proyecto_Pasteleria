from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from Backend.models import UserCreate, LoginRequest
from Backend.services.auth import create_access_token, get_db, verify_password,get_password_hash
from Backend.models import User
from sqlalchemy.orm import Session

route = APIRouter()


templates = Jinja2Templates(directory="Frontend/templates")

@route.get("/register/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("register.html",{"request": request})




@route.post("/register/")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        # Aquí deberías agregar la lógica para crear el usuario en la base de datos
        # por ejemplo, utilizando el modelo UserCreate para validar los datos
        user = create_user(db, user_data)  # Tu lógica para crear un usuario
        return {"message": "Usuario registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")