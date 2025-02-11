

from fastapi import APIRouter, Depends
from requests import Session
from Backend.db.database import get_db
from Backend.models.user_model import Pedido
from Backend.schemas.schema_pedido import PedidoCreate


route = APIRouter()

@route.post("/guardarOrden/")
async def guardar_orden(pedido: PedidoCreate, db: Session = Depends(get_db)):
    # Crear un nuevo pedido a partir de los datos recibidos
    db_pedido = Pedido(
        tematica=pedido.tematica,
        cake_type=pedido.cake_type,
        cake_shape=pedido.cake_shape,
        cake_size=pedido.cake_size,
        decoration=pedido.decoration,
        message=pedido.message,
        image_url=pedido.imagenSeleccionada,
        pastelero_id=pedido.pastelero_id,
        status="Pendiente"  # Estado inicial
    )

    # Guardar el nuevo pedido en la base de datos
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)  # Refresca el objeto para obtener el ID

    return {"message": "Orden guardada con éxito", "pedido_id": db_pedido.id}