from typing import List
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Modelo de usuario
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    client_id = Column(String)
    phone_number = Column(String)
    email = Column(String, unique=True, index=True)

# Definir un esquema para los datos de registro
class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    
    phone_number: str
    email: EmailStr

class LoginRequest(BaseModel):
    username: str
    password: str



