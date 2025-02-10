from io import BytesIO
from fastapi.responses import StreamingResponse
import httpx
from Backend.schemas.schema_cake import cakeDataRequest
from Backend.utils.config import API_URL,API_KEY
from fastapi import HTTPException
import time

async def generate_cake_image(request: cakeDataRequest):
    prompt = (          f"Un pastel con la siguiente descripción:\n"
                        f"Temática: {request.tematica}\n"
                        f"Sabor: {request.cake_type}\n"
                        f"Tamaño: {request.cake_size}\n"
                        f"Decoración: {request.decoration}\n"
                        f"Mensaje en el pastel: {request.message}\n"
                         "Por favor, crea una imagen que represente este pastel."
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
    generation_id= result.get("sdGenerationJob",{}).get("generationId")  # Esto debe ser una lista de URLs

    print("GEERATION ID=", generation_id)

    if not generation_id:
        raise HTTPException(status_code=500, detail="No se recibieron URLs de imágenes.")

    return await check_status(generation_id)




async def check_status(generation_id: str):
    url = f"{API_URL}/{generation_id}"
    headers = {"authorization": f"Bearer {API_KEY}"}

    # Realizamos un bucle de verificación hasta que el estado sea "COMPLETE"
    while True:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        result = response.json()
        generations_data = result.get("generations_by_pk", {})

        if not generations_data:
            raise HTTPException(status_code=500, detail="No se encontraron datos de generación")

        status = generations_data.get("status")
        if status == "COMPLETE":
            break  # Sale del bucle si está completo
        elif status == "FAILED":
            raise HTTPException(status_code=500, detail="La generación de la imagen falló")
        
        # Si el estado es "PENDING", espera 2 segundos y vuelve a intentar
        time.sleep(2)  # Espera 2 segundos antes de volver a hacer la solicitud

    # Una vez completado, obtiene las imágenes generadas
    generated_images = generations_data.get("generated_images", [])
    if not generated_images:
        raise HTTPException(status_code=500, detail="No se encontraron imágenes generadas.")

    image_urls = [image.get("url") for image in generated_images if image.get("url")]

    if not image_urls:
        raise HTTPException(status_code=500, detail="No se encontraron URLs de imágenes generadas.")

    return {"generated_images": [{"url": url} for url in image_urls]}
