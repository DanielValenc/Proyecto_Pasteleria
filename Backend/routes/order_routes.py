

import random
from fastapi import APIRouter, Depends
from requests import Session
from Backend.db.database import get_db
from Backend.models.user_model import Pedido, UsersRequest
from Backend.schemas.schema_pedido import PedidoCreate


route = APIRouter()

@route.post("/guardarOrden/")
async def guardar_orden(pedido: PedidoCreate, db: Session = Depends(get_db)):
    # Validación de campos
    if not pedido.tematica:
        return {"error": "La temática es obligatoria"}
    if not pedido.cake_type:
        return {"error": "El sabor y relleno son obligatorios"}
    if not pedido.cake_shape:
        return {"error": "La forma del pastel es obligatoria"}
    if not pedido.cake_size:
        return {"error": "El tamaño del pastel es obligatorio"}
    if not pedido.decoration:
        return {"error": "La decoración es obligatoria"}

    # Si el mensaje está vacío, lo dejamos como None
    if not pedido.message:
        pedido.message = None

    # Crear un nuevo pedido a partir de los datos recibidos
    db_pedido = Pedido(
        tematica=pedido.tematica,
        cake_type=pedido.cake_type,
        cake_shape=pedido.cake_shape,
        cake_size=pedido.cake_size,
        decoration=pedido.decoration,
        message=pedido.message,
        image_url=pedido.image_url,
        pastelero_id=pedido.pastelero_id,
    )
    print(db_pedido)
    # Guardar el nuevo pedido en la base de datos
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)  # Refresca el objeto para obtener el ID
    

    return {"message": "Orden guardada con éxito", "pedido_id": db_pedido.id}



@route.get("/pastelero-random/")
def get_random_pastelero(db: Session = Depends(get_db)):
    pasteleros = db.query(UsersRequest.id).filter(UsersRequest.role == "pastelero").all()
    if not pasteleros:
        return {"error": "No hay pasteleros disponibles"}
    pastelero_id = random.choice([p[0] for p in pasteleros])
    return {"pastelero_id": pastelero_id}
