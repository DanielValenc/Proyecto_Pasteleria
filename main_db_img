from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from b2sdk.v2 import InMemoryAccountInfo, B2Api
from io import BytesIO
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuración de la API externa
API_URL = "https://cloud.leonardo.ai/api/rest/v1/generations"
API_KEY = "57c8daa0-ec4e-4997-9f9c-73399336062a"

# Configuración de Backblaze B2
B2_KEY_ID = "0057a8127d9f9f30000000001"
B2_APPLICATION_KEY = "K005pRjlU3f/QjlwXFI9xes6lvEtbKM"
BUCKET_NAME = "Imagenes-G5"

# Inicializa la API de Backblaze
info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", B2_KEY_ID, B2_APPLICATION_KEY)
bucket = b2_api.get_bucket_by_name(BUCKET_NAME)

# Modelo para la solicitud de personalización
class CakeCustomizationRequest(BaseModel):
    personalizacion: str
    sabores: str
    forma: str
    adornos: str

# Configuración de la base de datos PostgreSQL
DATABASE_URL = "postgresql://postgres:Davidvilla7997@localhost/users_tartamia"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de usuario
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    client_id = Column(Integer, unique=True)
    phone_number = Column(String, unique=True)
    email = Column(String, unique=True)

# Definir un esquema para los datos de registro
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

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Configuración de seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name,
        client_id=user.client_id,
        phone_number=user.phone_number,
        email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Redirigir al login.html tras el registro
    return RedirectResponse(url="/static/login.html", status_code=303)

@app.post("/login/")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    access_token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    # Redirigir al index.html tras el inicio de sesión
    return RedirectResponse(url="/static/index.html", status_code=303)



@app.post("/generate-cake-image/")
async def generate_cake_image(request: CakeCustomizationRequest):
    """
    Crea un prompt basado en las características del pastel, solicita la generación de la imagen,
    y obtiene un token de generación para usar luego con el check-status.
    """
    # Construir el prompt
    prompt = (
        f"Genera un pastel de {request.personalizacion} de sabor {request.sabores}, "
        f"con forma {request.forma} y decorado con {request.adornos}."
    )

    # Configuración del payload para la API externa
    payload = {
        "prompt": prompt,
        "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",  # Reemplaza con el ID de modelo adecuado
        "width": 512,
        "height": 512,
    }
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {API_KEY}",
        "content-type": "application/json"
    }

    # Enviar la solicitud a la API externa
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    # Obtener el resultado de la API
    result = response.json()
    # Acceder al generation_id dentro del objeto 'sdGenerationJob'
    generation_id = result.get("sdGenerationJob", {}).get("generationId")
    
    # Depuración en caso de que no se reciba el generation_id
    if not generation_id:
        raise HTTPException(status_code=500, detail=f"No se recibió el generation_id. Respuesta: {result}.")

    # Retornar el generation_id para usar en el check-status
    return {"generation_id": generation_id}

@app.get("/check-status/{generation_id}")
async def check_status(generation_id: str):
    """
    Consulta el estado de una generación de imagen usando el generation_id
    y descarga las imágenes generadas desde las URLs.
    """
    url = f"{API_URL}/{generation_id}"
    headers = {
        "authorization": f"Bearer {API_KEY}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    result = response.json()
    generations_data = result.get("generations_by_pk", {})

    if not generations_data:
        raise HTTPException(status_code=500, detail="No se encontraron datos de generación.")

    status = generations_data.get("status")
    if not status:
        raise HTTPException(status_code=500, detail="No se encontró el estado de la generación.")

    if status != "COMPLETE":
        return {"status": status}

    generated_images = generations_data.get("generated_images", [])
    if not generated_images:
        raise HTTPException(status_code=500, detail="No se encontraron imágenes generadas.")

    uploaded_files = []

    for idx, image in enumerate(generated_images):
        image_url = image.get("url")
        if not image_url:
            continue

        async with httpx.AsyncClient() as client:
            image_response = await client.get(image_url)

        if image_response.status_code != 200:
            raise HTTPException(status_code=image_response.status_code, detail="Error al descargar la imagen generada.")

        file_name = f"pasteles/{generation_id}_image_{idx}.jpg"
        bucket.upload_bytes(image_response.content, file_name)

        # Generar el enlace público con la URL correcta para el bucket
        public_url = f"https://f005.backblazeb2.com/file/{BUCKET_NAME}/{file_name}"
        uploaded_files.append(public_url)

    return {"status": "COMPLETE", "uploaded_files": uploaded_files}



@app.get("/")
async def read_root():
    return {"message": "Welcome to my FastAPI project!"}



#uvicorn main:app --reload