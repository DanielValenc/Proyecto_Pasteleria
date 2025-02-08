import httpx
from Backend.schemas.modelDataCake import cakeDataRequest
from Backend.config import API_URL,API_KEY
from fastapi import HTTPException


async def generate_cake_image(request: cakeDataRequest):
    prompt = ( f"Diseña un pastel con la siguiente información:La temática del pastel tiene {request.tematica} La forma del pastel es {request.forma}, "
               f"con {request.porciones} porciones. Tiene una cubierta de {request.cubierta} y va tener una distribución de {request.distribucion}."
               f"La decoración incluye {',' .join(request.decoracion)} combinado con los siguientes colores {request.color}. Además, lleva un mensaje que dice: {request.mensaje}"
               f"El diseño debe ser factible para un pastelero profesional y visualmente atractivo."
             )

    payload = {
        "prompt": prompt,
        #Nombre del modelo:
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

    result = response.json()

    # Suponiendo que la respuesta contiene una lista de URLs de imágenes
    image_urls = result.get("imageUrls")  # Esto debe ser una lista de URLs

    print(image_urls)

    if not image_urls:
        raise HTTPException(status_code=500, detail="No se recibieron URLs de imágenes.")

    return {"image_urls": image_urls}



async def check_generation_status(generation_id: str):
    url = f"{API_URL}/{generation_id}"
    headers = {"authorization": f"Bearer {API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return response.json()
