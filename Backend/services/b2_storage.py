from b2sdk.v2 import B2Api, InMemoryAccountInfo
from fastapi import HTTPException, requests
from requests import Session
from Backend.models.user_model import UsersRequest
from Backend.utils.config import B2_APP_KEY,B2_KEY_ID,B2_BUCKET_NAME

# Función para crear una carpeta en Backblaze
def create_backblaze_folder(correo: str, db: Session):
    try:
        # Cargar credenciales de Backblaze
        b2_info = InMemoryAccountInfo()
        b2_api = B2Api(b2_info)

        b2_api.authorize_account("production", B2_KEY_ID, B2_APP_KEY)

        # Obtener el bucket de Backblaze
        bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)

        # Crear un nombre para la "carpeta" usando el correo del usuario (agregar barra al final)
        folder_name = f"{correo}"  # Carpeta representada por un archivo con barra final
        file_name = f"{folder_name}"  # Usamos el nombre del archivo para simular la carpeta

        try:
            # Verificar si el "archivo" (simulación de carpeta) ya existe en el bucket
            bucket.get_file_info_by_name(file_name)
            print(f"La carpeta para el usuario {correo} ya existe en Backblaze.")
        except Exception:
            # Si no existe, crear un archivo vacío para simular la "carpeta"
            print(f"Creando la carpeta para el usuario {correo} en Backblaze...")
            file_info = bucket.upload_bytes(b" ", file_name)  # Subimos un archivo vacío
            print(f"Archivo subido correctamente: {file_info}")

            # Asociamos la carpeta con el usuario en la base de datos
            usuario_existente = db.query(UsersRequest).filter(UsersRequest.correo == correo).first()
            if usuario_existente:
                usuario_existente.backblaze_folder_created = True
                db.commit()

    except Exception as e:
        print(f"Error al crear la carpeta en Backblaze: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear la carpeta en Backblaze: {e}")
    


def get_b2_auth():
    auth_url = "https://api.backblazeb2.com/b2api/v2/b2_authorize_account"
    response = requests.get(auth_url, auth=(B2_ACCOUNT_ID, B2_APP_KEY))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Error en autenticación con Backblaze B2")

# Función para subir imagen desde una URL a Backblaze B2
def upload_image(image_url, user_email):
    auth_data = get_b2_auth()
    upload_url = f"{auth_data['apiUrl']}/b2api/v2/b2_get_upload_url"
    headers = {"Authorization": auth_data["authorizationToken"]}
    
    # Obtener URL de subida
    upload_response = requests.post(upload_url, json={"bucketId": auth_data["allowed"]["bucketId"]}, headers=headers)
    upload_data = upload_response.json()
    
    # Descargar la imagen
    image_response = requests.get(image_url)
    if image_response.status_code != 200:
        raise Exception("No se pudo descargar la imagen")

    # Configurar el nombre del archivo en Backblaze
    file_name = f"{user_email}/{image_url.split('/')[-1]}"
    upload_headers = {
        "Authorization": upload_data["authorizationToken"],
        "X-Bz-File-Name": file_name,
        "Content-Type": "image/jpeg",
        "X-Bz-Content-Sha1": "do_not_verify"
    }

    # Subir la imagen
    upload_file_response = requests.post(upload_data["uploadUrl"], headers=upload_headers, data=image_response.content)
    if upload_file_response.status_code == 200:
        return f"https://f005.backblazeb2.com/file/{B2_BUCKET_NAME}/{file_name}"
    else:
        raise Exception("Error al subir la imagen a Backblaze B2")    