from pydantic import BaseModel


class PedidoCreate(BaseModel):
    tematica: str
    cake_type: str
    cake_shape: str
    cake_size: str
    decoration: str
    message: str
    imagenSeleccionada: str
    pastelero_id: int
    tiempo_espera: int
