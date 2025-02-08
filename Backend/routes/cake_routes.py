from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from Backend.models import CakeCustomizationRequest
from Backend.services.image_generator import generate_cake_image as generate_image_service, check_generation_status
from fastapi.templating import Jinja2Templates

route = APIRouter()

templates = Jinja2Templates(directory="Frontend/templates")

# Ruta para cargar la página del formulario
@route.get("/generate/", response_class=HTMLResponse)
async def generate_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Ruta corregida para recibir los datos del formulario y generar la imagen
@route.post("/generate-cake-image/")
async def generate_cake(request: CakeCustomizationRequest):
    print("Solicitud recibida:", request)
    return await generate_image_service(request)  # Llamamos al servicio de generación

# Ruta para verificar el estado de la generación de la imagen
@route.get("/check-status/{generation_id}")
async def check_status(generation_id: str):
    return await check_generation_status(generation_id)
