from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
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

@app.get("/", response_class=HTMLResponse)
async def serve_html():
    with open("templates/index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/generate-cake-image/")
async def generate_cake_image(request: CakeCustomizationRequest):
    prompt = (
        f"Haz un pastel de {request.personalizacion} con sabor {request.sabores}, la forma del pastel es {request.forma} y el decorado externo con {request.adornos}."
    )

    payload = {
        "prompt": prompt,
        "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
        "width": 512,
        "height": 512,
    }
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {API_KEY}",
        "content-type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    # Asumimos que la API devuelve la URL de la imagen en "imageUrl"
    image_url = data.get("imageUrl")
    if not image_url:
        raise HTTPException(status_code=500, detail="La API no devolvió la URL de la imagen.")

    return {"image_url": image_url}
