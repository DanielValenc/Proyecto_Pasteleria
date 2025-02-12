from fastapi import APIRouter,  Request
from fastapi.responses import HTMLResponse
from Backend.schemas.schema_cake import cakeDataRequest
from Backend.services.image_generator import generate_cake_image
from fastapi.templating import Jinja2Templates

route = APIRouter()


templates = Jinja2Templates(directory="Frontend/templates/cliente")

@route.get("/generate/" , response_class=HTMLResponse)
async def generateForm(request: Request ):
   
   return templates.TemplateResponse("generar_pastel.html",{"request":request})



@route.post("/generate/")
async def generate_cake(request: cakeDataRequest):
    print("📢 Datos JSON recibidos:", request) 
    return await   generate_cake_image(request)



