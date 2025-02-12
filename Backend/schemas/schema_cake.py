from pydantic import BaseModel

class cakeDataRequest(BaseModel):
    tematica: str
    cake_type: str
    cake_shape:str
    cake_size: str
    decoration: str
    message:str = None
    
    
  