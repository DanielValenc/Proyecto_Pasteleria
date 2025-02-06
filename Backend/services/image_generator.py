import httpx
from Backend.models import CakeCustomizationRequest
from Backend.services.b2_storage import upload_to_b2
from Backend.config import API_URL,API_KEY
from fastapi import HTTPException


async def generate_cake_image(request: CakeCustomizationRequest):
    prompt = f"Genera un pastel de {request.personalizacion} de sabor {request.sabores}, con forma {request.forma} y decorado con {request.adornos}."
    
    payload = {
        "prompt": prompt,
        "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3", 
        "width": 512,
        "height": 512,
    }
    headers = {"accept": "application/json", "authorization": f"Bearer {API_KEY}", "content-type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    result = response.json()
    generation_id = result.get("sdGenerationJob", {}).get("generationId")
    
    if not generation_id:
        raise HTTPException(status_code=500, detail="No se recibió el generation_id.")
    
    return {"generation_id": generation_id}

async def check_generation_status(generation_id: str):
    url = f"{API_URL}/{generation_id}"
    headers = {"authorization": f"Bearer {API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return response.json()
