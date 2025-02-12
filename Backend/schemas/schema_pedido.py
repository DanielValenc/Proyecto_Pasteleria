from typing import Optional
from pydantic import BaseModel

class PedidoCreate(BaseModel):
    tematica: str
    cake_type: str  # Cambiar a cake_type para que coincida con el modelo ORM
    cake_shape: str  # Cambiar a cake_shape
    cake_size: str  # Cambiar a cake_size
    decoration: str  # Cambiar a decoration
    message: Optional[str] = None # Cambiar a message
    image_url: str  # Cambiar a image_url
    pastelero_id: int

    class Config:
        orm_mode = True
        from_attributes = True
