from fastapi import APIRouter, Depends, HTTPException, Query, requests
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from Backend.services.b2_storage import upload_image
from Backend.schemas.schemaa_img import ImageUploadRequest
from Backend.utils.config import B2_APP_KEY, B2_KEY_ID, B2_BUCKET_NAME



route = APIRouter()


templates = Jinja2Templates(directory="Frontend/templates")



@route.post("/upload_image_and_redirect/")
async def upload_image_and_redirect(request: ImageUploadRequest):
    try:
        # Subir la imagen a Backblaze B2
        uploaded_url = upload_image(request.imageUrl, request.userEmail)
        return {"uploadedImageUrl": uploaded_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))