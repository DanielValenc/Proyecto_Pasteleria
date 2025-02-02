from fastapi import FastAPI, Form, Request 
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app=FastAPI()



app.mount("/static", StaticFiles(directory="Frontend/static"), name="static")

templates = Jinja2Templates(directory="Frontend/templates")

# Ruta principal
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("home.html",{"request": request})


# Ruta para la página del formulario (form.html)
@app.get("/form", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.get("/products", response_class=HTMLResponse)
async def read_contact(request: Request):
    return templates.TemplateResponse("products.html", {"request": request})

# Ruta para la página de contacto (contact.html)
@app.get("/contact", response_class=HTMLResponse)
async def read_contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})




