
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Backend.db.database import get_db
from Backend.models.user_model import UsersRequest

route = APIRouter()


templates = Jinja2Templates(directory="Frontend/templates")

@route.get("/register/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("register.html",{"request": request})


@route.post("/register/")
async def registrar_usuario(
    nombre: str = Form(...),
    apellido: str = Form(...),
    celular: str = Form(...),
    correo: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
   # Validación de campos vacíos
    if not nombre.strip() or not apellido.strip() or not celular.strip() or not correo.strip() or not password.strip():
        return JSONResponse(content={"error": "Todos los campos son requeridos."}, status_code=400)

    # Verificar si el correo ya está registrado
    usuario_existente = db.query(UsersRequest).filter(UsersRequest.correo == correo).first()
    if usuario_existente:
        return JSONResponse(content={"error": "El correo ya está registrado."}, status_code=400)

    nuevo_usuario = UsersRequest(
        nombre=nombre,
        apellido=apellido,
        celular=celular,
        correo=correo,
        password=password  # Aquí puedes agregar el hash si decides hacerlo
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
     # Redirigir al usuario al login después de registrarse
    # Si el registro fue exitoso, devolvemos un mensaje de éxito
    return JSONResponse(content={"message": "Usuario registrado correctamente"}, status_code=200)


