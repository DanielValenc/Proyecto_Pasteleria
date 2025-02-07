from typing import List
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    client_id = Column(Integer, unique=True)
    phone_number = Column(String, unique=True)
    email = Column(String, unique=True)

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    client_id: int
    phone_number: str
    email: EmailStr

class LoginRequest(BaseModel):
    username: str
    password: str

class CakeCustomizationRequest(BaseModel):
    #pastelero_id: str
    forma: str
    porciones:str
    cubierta: str
    distribucion:str
    decoracion: List[str]
    mensajePastel: str
    personalizacion:str

