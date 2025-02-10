# Definir un esquema para los datos de registro
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    nombre: str
    apellido: str
    celular: str
    correo: EmailStr
    password: str

class LoginRequest(BaseModel):
    correo: EmailStr
    password: str