import requests

url = "https://cloud.leonardo.ai/api/rest/v1/platformModels"

headers = {
    "accept": "application/json",
    "authorization": "Bearer 57c8daa0-ec4e-4997-9f9c-73399336062a"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("Modelos disponibles:")
    
    # Iterar a través de cada modelo y extraer detalles
    for model in data.get("custom_models", []):
        model_id = model.get('id', 'No disponible')  # Extraer el ID del modelo
        name = model.get('name', 'No disponible')
        description = model.get('description', 'No disponible')
        image_url = model.get('image', 'No disponible')
        
        # Mostrar los detalles de cada modelo
        print(f"\nID: {model_id}")
        print(f"Modelo: {name}")
        print(f"Descripción: {description}")
        print(f"Imagen: {image_url}")
        print("-" * 40)  # Separador visual para mejor claridad

else:
    print(f"Error {response.status_code}: {response.text}")