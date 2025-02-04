from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import httpx
from b2sdk.v2 import InMemoryAccountInfo, B2Api

app = FastAPI()

# Configuración de la API externa
API_URL = "https://cloud.leonardo.ai/api/rest/v1/generations"
API_KEY = "57c8daa0-ec4e-4997-9f9c-73399336062a"

# Configuración de Backblaze B2
B2_KEY_ID = "0057a8127d9f9f30000000001"
B2_APPLICATION_KEY = "K005pRjlU3f/QjlwXFI9xes6lvEtbKM"
BUCKET_NAME = "Imagenes-G5"

# Inicializa la API de Backblaze
info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", B2_KEY_ID, B2_APPLICATION_KEY)
bucket = b2_api.get_bucket_by_name(BUCKET_NAME)

# Configuración para servir la interfaz HTML
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class CakeCustomizationRequest(BaseModel):
    personalizacion: str
    sabores: str
    forma: str
    adornos: str


@app.get("/", response_class=HTMLResponse)
async def render_form(request: Request):
    """Renderiza la interfaz HTML para personalizar y generar pasteles."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate-cake-image/")
async def generate_cake_image(request: CakeCustomizationRequest):
    """
    Genera un pastel personalizado basado en las opciones del usuario
    y devuelve el ID de generación.
    """
    prompt = (
        f"Genera un pastel de {request.personalizacion} de sabor {request.sabores}, "
        f"con forma {request.forma} y decorado con {request.adornos}."
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
        "content-type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    result = response.json()
    generation_id = result.get("sdGenerationJob", {}).get("generationId")

    if not generation_id:
        raise HTTPException(
            status_code=500, detail=f"No se recibió el generation_id. Respuesta: {result}."
        )

    return {"generation_id": generation_id}


@app.get("/check-status/{generation_id}")
async def check_status(generation_id: str):
    """
    Consulta el estado de generación de imagen y descarga las imágenes generadas.
    """
    url = f"{API_URL}/{generation_id}"
    headers = {"authorization": f"Bearer {API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    result = response.json()
    generations_data = result.get("generations_by_pk", {})

    if not generations_data:
        raise HTTPException(status_code=500, detail="No se encontraron datos de generación.")

    status = generations_data.get("status")

    if status != "COMPLETE":
        raise HTTPException(status_code=500, detail=f"Generación en proceso. Estado actual: {status}")

    generated_images = generations_data.get("generated_images", [])
    if not generated_images:
        raise HTTPException(status_code=500, detail="No se encontraron imágenes generadas.")

    uploaded_files = []

    for idx, image in enumerate(generated_images):
        image_url = image.get("url")
        if not image_url:
            raise HTTPException(status_code=500, detail="No se encontró la URL de la imagen generada.")

        async with httpx.AsyncClient() as client:
            image_response = await client.get(image_url)

        if image_response.status_code != 200:
            raise HTTPException(status_code=image_response.status_code, detail="Error al descargar la imagen generada.")

        file_name = f"pasteles/{generation_id}_image_{idx}.jpg"
        bucket.upload_bytes(image_response.content, file_name)
        uploaded_files.append(file_name)

    public_url = f"https://f002.backblazeb2.com/file/{BUCKET_NAME}/{uploaded_files[0]}"
    return {"message": "Imágenes generadas y almacenadas exitosamente.", "uploaded_files": uploaded_files}

