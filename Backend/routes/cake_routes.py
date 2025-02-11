from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from requests import Session
from Backend.db.database import get_db
from Backend.models.user_model import Pedido
from Backend.schemas.schema_cake import cakeDataRequest
from Backend.services.image_generator import generate_cake_image, check_status
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



@route.get("/check-status/{generation_id}")
async def status_image(generation_id: str):
    return await check_status(generation_id)


@route.get("/pastelero/pedidos/")
async def ver_pedidos(db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.status == "Pendiente").all()
    return {"pedidos": pedidos}

@route.post("/pastelero/aceptar_pedido/{pedido_id}")
async def aceptar_pedido(pedido_id: int, pastelero_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    pedido.pastelero_id = pastelero_id
    pedido.status = "En proceso"
    db.commit()
    return {"message": "Pedido aceptado"}