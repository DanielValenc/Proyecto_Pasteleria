from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from transformers import pipeline
import uvicorn
import requests
import os
from dotenv import load_dotenv 

load_dotenv()
API_KEY=os.getenv("API_KEY")

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")



# Ruta principal
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})



# Generar imagen con IA
@app.post("/generate/", response_class=HTMLResponse)
async def generate(
    request: Request, 
    porciones: str = Form(...),
    forma: str = Form(...),
    sabor: str = Form(...),
    topping: str = Form(...), 
    tematica: str = Form(...),
    color: str =Form(...),
    estilo: str = Form(...),
    decoracion: str = Form(...),
    mensaje: str = Form(None)
    ):
  
   
    # Crear el prompt basado en los datos del formulario
    prompt = (
        f"Un pastel con {porciones} porciones, en forma de {forma}, "
        f", cubierto con{topping}, con temática {tematica}, "
        f"con colores {color}, , con estilo {estilo},decorado con {decoracion}. "
    )
    if mensaje:
        prompt += f"Message on the cake: {mensaje}"

    # Mostrar el prompt en consola
    print(f"Prompt: {prompt}")

    # Configurar la solicitud a la API de DreamStudio
    api_url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,  # Ajusta la precisión creativa (6-15 recomendado)
        "clip_guidance_preset": "FAST_BLUE",  # Mejora los detalles visuales
        "height": 512,
        "width": 512,
        "samples": 1,
    }

    # Realizar la solicitud a la API
    response = requests.post(api_url, headers=headers, json=payload)

       # Manejar la respuesta
    if response.status_code == 200:
         result = response.json()
         image_url = result["artifacts"][0]["url"]  # URL de la imagen generada
         return templates.TemplateResponse(
                "base.html", 
                 {"request": request, "image_url": image_url}
         )
    else:
         error_message = response.json().get("message", "Error al generar la imagen.")
         return templates.TemplateResponse(
               "base.html", 
              {"request": request, "msg": error_message}
         )

