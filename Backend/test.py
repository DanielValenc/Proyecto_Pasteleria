from b2sdk.v2 import B2Api, InMemoryAccountInfo
from fastapi import HTTPException
from requests import Session
from Backend.models.user_model import UsersRequest
from utils.config import B2_APP_KEY, B2_KEY_ID, B2_BUCKET_NAME

# Función para crear una "carpeta" en Backblaze (subiendo un archivo vacío)
def create_backblaze_folder(correo: str, db: Session):
    try:
        # Cargar credenciales de Backblaze
        b2_info = InMemoryAccountInfo()
        b2_api = B2Api(b2_info)

        # Autenticar con Backblaze
        b2_api.authorize_account("production", B2_KEY_ID, B2_APP_KEY)

        # Obtener el bucket de Backblaze
        bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)

        # Nombre de la "carpeta" en Backblaze
        folder_name = f"{correo}/"  # La carpeta se representa como un nombre de archivo con barra
        file_name = f"{folder_name}empty.txt"  # Un archivo vacío en la "carpeta"

        # Comprobar si el archivo ya existe
        try:
            # Intentar acceder al archivo (esto nos permitirá verificar si la "carpeta" ya existe)
            bucket.get_file_info_by_name(file_name)
            print(f"La carpeta para el usuario {correo} ya existe en Backblaze.")
        except Exception:
            # Si el archivo no existe, lo creamos
            print(f"Creando la carpeta para el usuario {correo} en Backblaze...")
            # Subir un archivo vacío
            file_info = bucket.upload_bytes(b" ", file_name)
            print(f"Archivo subido correctamente: {file_info}")
            # Ahora, asociamos la carpeta al usuario en la base de datos, si es necesario.
            usuario_existente = db.query(UsersRequest).filter(UsersRequest.correo == correo).first()
            if usuario_existente:
                usuario_existente.backblaze_folder_created = True
                db.commit()

    except Exception as e:
        print(f"Error al crear la carpeta en Backblaze: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear la carpeta en Backblaze: {e}")
