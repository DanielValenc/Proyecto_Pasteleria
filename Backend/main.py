from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from Backend.routes.login_routes import route as login_route
from Backend.routes.register_routes import route as register_route
from Backend.routes.cake_routes import route as cake_route
from Backend.routes.home_routes import route as home_route
from Backend.routes.products_routes import route as products_route
from Backend.routes.profile_routes import route as profile_route

from fastapi.staticfiles import StaticFiles
import os



app = FastAPI()

# Llama a la función de crear la base de datos al iniciar la app

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],  # Puedes especificar un conjunto de orígenes si prefieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="Frontend/static"), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/login/")


app.include_router(login_route)
app.include_router(home_route)
app.include_router(cake_route)
app.include_router(profile_route)
app.include_router(products_route)
app.include_router(register_route)




