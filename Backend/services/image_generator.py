import httpx
from fastapi import HTTPException
from Backend.models import CakeCustomizationRequest
from Backend.services.b2_storage import upload_to_b2
from Backend.config import API_URL, API_KEY, BUCKET_NAME, B2_KEY_ID, B2_APPLICATION_KEY
from b2sdk.v2 import InMemoryAccountInfo, B2Api

# Inicialización de Backblaze B2
info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", B2_KEY_ID, B2_APPLICATION_KEY)
bucket = b2_api.get_bucket_by_name(BUCKET_NAME)


async def generate_cake_image(request: CakeCustomizationRequest):
    """Genera una imagen de pastel basada en la solicitud del usuario."""
    prompt = (
        f"Diseña un pastel con la forma {request.forma}, {request.porciones} porciones, "
        f"cubierta de {request.cubierta}, distribución {request.distribucion}. "
        f"Decoración: {', '.join(request.decoracion)}. Mensaje: {request.mensajePastel}. "
        f"Personalización: {request.personalizacion}. El diseño debe ser factible y atractivo."
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

    result = response.json()
    generation_id = result.get("sdGenerationJob", {}).get("generationId")
    if not generation_id:
        raise HTTPException(status_code=500, detail="No se recibió el generation_id.")

    return {"generation_id": generation_id}


async def check_generation_status(generation_id: str):
    """Consulta el estado de la generación de la imagen."""
    url = f"{API_URL}/{generation_id}"
    headers = {"authorization": f"Bearer {API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


async def check_status(generation_id: str):
    """Obtiene el estado y, si está completo, sube las imágenes generadas a Backblaze B2."""
    result = await check_generation_status(generation_id)
    generations_data = result.get("generations_by_pk", {})

    if not generations_data:
        raise HTTPException(status_code=500, detail="No se encontraron datos de generación.")

    status = generations_data.get("status")
    if status != "COMPLETE":
        return {"status": status}

    generated_images = generations_data.get("generated_images", [])
    if not generated_images:
        raise HTTPException(status_code=500, detail="No se encontraron imágenes generadas.")

    uploaded_files = []
    for idx, image in enumerate(generated_images):
        image_url = image.get("url")
        if not image_url:
            continue

        async with httpx.AsyncClient() as client:
            image_response = await client.get(image_url)

        if image_response.status_code != 200:
            raise HTTPException(status_code=image_response.status_code, detail="Error al descargar la imagen.")

        file_name = f"pasteles/{generation_id}_image_{idx}.jpg"
        bucket.upload_bytes(image_response.content, file_name)

        public_url = f"https://f005.backblazeb2.com/file/{BUCKET_NAME}/{file_name}"
        uploaded_files.append(public_url)

    return {"status": "COMPLETE", "uploaded_files": uploaded_files}
