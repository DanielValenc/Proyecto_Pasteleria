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
    return templates.TemplateResponse("step1.html", {"request": request})
# Ruta para el segundo paso
@app.post("/step2/", response_class=HTMLResponse)
async def step2(request: Request, flavor: str = Form(...)):
    return templates.TemplateResponse("step2.html", {"request": request, "flavor": flavor})
    return templates.TemplateResponse("base.html", {"request": request})

# Ruta para el tercer paso
@app.post("/step3/", response_class=HTMLResponse)
async def step3(request: Request, shape: str = Form(...), flavor: str = Form(...)):
    return templates.TemplateResponse("step3.html", {"request": request, "shape": shape, "flavor": flavor})
# Step 3
@app.post("/generate/")
async def generate_cake(request: Request, flavor: str = Form(...), shape: str = Form(...), topping: str = Form(...)):
    # Pasa los datos a la nueva página de resumen
    return templates.TemplateResponse(
        "summary.html",
        {"request": request, "flavor": flavor, "shape": shape, "topping": topping}
    )


# Generar imagen con IA
@app.post("/generate/", response_class=HTMLResponse)
async def generate(request: Request, topping: str = Form(...), shape: str = Form(...), flavor: str = Form(...)):
    # Simulación con Transformers (puedes personalizar este paso)
    model = pipeline("text-to-image-generation")
    prompt = f"A {shape} cake with {flavor} flavor and {topping} topping"
    generated_image = model(prompt)
    return templates.TemplateResponse("result.html", {"request": request, "image": generated_image, "prompt": prompt})
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
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
  