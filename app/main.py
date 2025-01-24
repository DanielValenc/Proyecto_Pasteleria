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
   
 # Imprimir los datos para verificar
    print(f"Porciones: {porciones}, Forma: {forma}, Sabor: {sabor}, Topping: {topping}, "
          f"Temática: {tematica}, Color: {color}, Estilo: {estilo}, Decoración: {decoracion}, Mensaje: {mensaje}")
    
    # Crear el prompt basado en los datos del formulario
    prompt = (
        f"A cake with {porciones} portions, in a {forma} shape, "
        f"flavored with {sabor}, topped with {topping}, themed as {tematica}, "
        f"colored {color}, styled as {estilo}, decorated with {decoracion}. "
    )
    if mensaje:
        prompt += f"Message on the cake: {mensaje}"

    # Mostrar el prompt en consola
    print(f"Prompt: {prompt}")

    # Configurar la solicitud a la API de DreamStudio
    api_url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-5/text-to-image"
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
        print(f"Imagen generada: {image_url}")
        return templates.TemplateResponse("base.html", {"request": request, "image_url": image_url})
    else:
        error_message = response.json().get("message", "Error al generar la imagen.")
        print(f"Error: {error_message}")
        return templates.TemplateResponse("base.html", {"request": request, "msg": error_message})