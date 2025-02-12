from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import  JSONResponse
from fastapi import  Request
from requests import Session

from Backend.db.database import get_db
from Backend.models.user_model import Pedido
from Backend.schemas.schema_pedido import PedidoCreate 


route = APIRouter()


templates = Jinja2Templates(directory="Frontend/templates/pastelero")

@route.get("/pastelero/pedidos/",response_class=JSONResponse)
async def obtener_pedidos_json(db: Session = Depends(get_db)):
    # Obtener todos los pedidos de la base de datos
    pedidos = db.query(Pedido).all()

    # Convertir los objetos Pedido a un diccionario usando Pydantic (PedidoCreate)
    return JSONResponse(content=[PedidoCreate.from_orm(pedido).dict() for pedido in pedidos])
