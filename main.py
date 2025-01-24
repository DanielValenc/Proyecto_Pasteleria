from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

# Configuración de la API externa
API_URL = "https://cloud.leonardo.ai/api/rest/v1/generations"
API_KEY = "57c8daa0-ec4e-4997-9f9c-73399336062a"

class CakeCustomizationRequest(BaseModel):
    personalizacion: str
    sabores: str
    forma: str
    adornos: str

# Modelo para el estado de generación
class GenerationStatus(BaseModel):
    generationId: str

@app.post("/generate-cake-image/")
async def generate_cake_image(request: CakeCustomizationRequest):
    """
    Crea un prompt basado en las características del pastel y solicita la generación de la imagen.
    """
    # Construir el prompt
    prompt = (
        f"Genera un pastel de {request.personalizacion} de sabor {request.sabores}, con forma {request.forma} y decorado con {request.adornos}."
    )

    # Configuración del payload para la API externa
    payload = {
        "prompt": prompt,
        "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",  # Reemplaza con el ID de modelo adecuado
        "width": 512,
        "height": 512,
    }
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {API_KEY}",
        "content-type": "application/json"
    }

    # Enviar la solicitud a la API externa
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


@app.get("/check-status/{generation_id}")
async def check_status(generation_id: str):
    """
    Consulta el estado de una generación de imagen usando el generationId.
    """
    url = f"{API_URL}/{generation_id}"
    headers = {
        "authorization": f"Bearer {API_KEY}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@app.get("/")
async def read_root():
    return {"message": "Welcome to my FastAPI project!"}