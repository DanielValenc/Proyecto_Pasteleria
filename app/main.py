from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from transformers import pipeline
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Ruta principal
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})



# Generar imagen con IA
@app.post("/generate/", response_class=HTMLResponse)
async def generate(
    request: Request, 
    porciones: str = Form(...),
    forma: str = Form(...),
    sabor: str = Form(...),
    topping: str = Form(...), 
    tematica: str = Form(...),
    color: str =Form(...),
    estilo: str = Form(...),
    decoracion: str = Form(...),
    mensaje: str = Form(None)
    ):
   
 # Imprimir los datos para verificar
    print(f"Porciones: {porciones}, Forma: {forma}, Sabor: {sabor}, Topping: {topping}, "
          f"Temática: {tematica}, Color: {color}, Estilo: {estilo}, Decoración: {decoracion}, Mensaje: {mensaje}")
   
    return templates.TemplateResponse("base.html", {"request": request, "msg": "Datos recibidos correctamente."})
  
