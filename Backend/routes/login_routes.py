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
templatesC = Jinja2Templates(directory="Frontend/templates/cliente")
templatesP = Jinja2Templates(directory="Frontend/templates/pastelero")

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

    
# Redirigir dependiendo del rol del usuario
    if usuario.role == "cliente":
        # Redirigir a la vista de cliente y devolver el role
        return JSONResponse(content={"role": "cliente", "redirect_url": "/cliente/panel"}, status_code=200)
    elif usuario.role == "pastelero":
        # Redirigir a la vista de pastelero y devolver el role
        return JSONResponse(content={"role": "pastelero", "redirect_url": "/pastelero/panel"}, status_code=200)
    else:
        return JSONResponse(content={"error": "Rol desconocido"}, status_code=400)



# Rutas para los paneles de cliente y pastelero

@route.get("/cliente/panel", response_class=HTMLResponse)
async def panel_cliente(request: Request):
    return templatesC.TemplateResponse("home.html", {"request": request})

@route.get("/pastelero/panel", response_class=HTMLResponse)
async def panel_pastelero(request: Request):
    return templatesP.TemplateResponse("dashboard_pastelero.html", {"request": request})