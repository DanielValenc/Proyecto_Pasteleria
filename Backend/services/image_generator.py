from io import BytesIO
from fastapi.responses import StreamingResponse
import httpx
from Backend.schemas.schema_cake import cakeDataRequest
from Backend.utils.config import API_URL,API_KEY
from fastapi import HTTPException
import time
from googletrans import Translator
 
async def generate_cake_image(request: cakeDataRequest):
    # Traducir los campos antes de construir el prompt
    tematica_en = traducir_a_ingles(request.tematica)
    cake_type_en = traducir_a_ingles(request.cake_type)
    cake_shape_en = traducir_a_ingles(request.cake_shape)
    cake_size_en = traducir_a_ingles(request.cake_size)
    decoration_en = traducir_a_ingles(request.decoration)
    message_en = traducir_a_ingles(request.message)

     # Ahora construimos el prompt en inglés
    prompt = (
                f"Generate an image of a cake with the following characteristics:\n"
                f"- Theme: {tematica_en} (e.g., birthday party, wedding, Christmas, Dragon Ball Z kids party, etc.)\n"
                f"- Flavor: {cake_type_en} (e.g., vanilla, chocolate, strawberry, vanilla with caramel filling, etc.)\n"
                f"- Shape: {cake_shape_en} (e.g., round, square, heart-shaped, etc.)\n"
                f"- Size: {cake_size_en} (e.g., large, medium, small, multi-layered, for 200 people (this means it's a large cake or it can be several cakes with the same design, emphasizing that it serves 200 people), etc.)\n"
                f"- Decoration: {decoration_en} (e.g., flowers, figures, colored icing, fruits, character figures, etc.)\n"
                f"- Message: {message_en} (e.g., Happy Birthday, Congratulations, etc.)\n"
                "Please create an image of a cake that reflects all these characteristics clearly and in detail, and keep in mind that everything is edible."
)



    payload = {
        "prompt": prompt,
        #Nombre del modelo:
        "modelId": "de7d3faf-762f-48e0-b3b7-9d0ac3a3fcf3", 
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



# Función para traducir a inglés
def traducir_a_ingles(texto: str) -> str:
    translator = Translator()
    traduccion = translator.translate(texto, src='es', dest='en')
    return traduccion.text