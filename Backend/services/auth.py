from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from requests import Session
from Backend.config import ALGORITHM,SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from Backend.database import SessionLocal
from Backend.models import User


# Configuración de seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funciones de autenticación
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    pass

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.email == username).first()  # Usa email si en tu base de datos es 'email'
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
