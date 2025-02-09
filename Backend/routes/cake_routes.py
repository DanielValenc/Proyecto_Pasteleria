from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from Backend.schemas.modelDataCake import cakeDataRequest
from Backend.services.image_generator import generate_cake_image, check_status
from fastapi.templating import Jinja2Templates

route = APIRouter()


templates = Jinja2Templates(directory="Frontend/templates")

@route.get("/generate/" , response_class=HTMLResponse)
async def generateForm(request: Request ):
   
   return templates.TemplateResponse("form.html",{"request":request})



@route.post("/generate/")
async def generate_cake(request: cakeDataRequest):
    print("📢 Datos JSON recibidos:", request) 
    return await   generate_cake_image(request)



@route.get("/check-status/{generation_id}")
async def status_image(generation_id: str):
    return await check_status(generation_id)
