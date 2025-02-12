from sqlalchemy import Column,  ForeignKey, Integer, String
from Backend.db.database import Base
from sqlalchemy.orm import relationship


class UsersRequest(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    celular = Column(String(15))
    correo = Column(String(100), unique=True)
    password = Column(String(255))
    role = Column(String(50), default="client")  # "client" o "pastelero"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    tematica = Column(String(255), nullable=False)
    cake_type = Column(String(255), nullable=False)
    cake_shape = Column(String(255), nullable=False)
    cake_size = Column(String(255), nullable=False)
    decoration = Column(String(255), nullable=False)
    message = Column(String(255), nullable=True)
    pastelero_id = Column(Integer, ForeignKey("users.id"))  # Relación con la tabla 'users'
    image_url = Column(String(500), nullable=True)

    pastelero = relationship("UsersRequest", foreign_keys=[pastelero_id])  # Relación con 'UsersRequest'

    # Para distinguir entre un pastelero y un cliente:
    @property
    def is_pastelero(self):
        return self.pastelero.role == "pastelero"
