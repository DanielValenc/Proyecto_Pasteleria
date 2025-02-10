from sqlalchemy import Column, Integer, String
from Backend.db.database import Base

class UsersRequest(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    celular = Column(String(15))
    correo = Column(String(100), unique=True)
    password = Column(String(255))




