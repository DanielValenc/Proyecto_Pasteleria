from fastapi import FastAPI
from Backend.routes.login_routes import router as login_router
from Backend.routes.auth_routes import router as auth_router
from Backend.routes.cake_routes import router as cake_router
from Backend.routes.home_routes import router as home_router
from fastapi.staticfiles import StaticFiles
import os


app = FastAPI()



app.mount("/static", StaticFiles(directory="Frontend/static"), name="static")

app.include_router(login_router)
app.include_router(home_router)
app.include_router(cake_router)
app.include_router(auth_router, prefix="/auth", tags=["auth"])



