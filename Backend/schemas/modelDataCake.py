from typing import List
from pydantic import BaseModel

class cakeDataRequest(BaseModel):
    tematica: str
    forma: str
    porciones:str
    cubierta: str
    distribucion:str
    decoracion: str
    color: str
    mensaje:str