from fastapi import FastAPI
from Backend.routes.login_routes import route as login_route
from Backend.routes.auth_routes import route as auth_route
from Backend.routes.cake_routes import route as cake_route
from Backend.routes.home_routes import route as home_route
from Backend.routes.products_routes import route as products_route
from Backend.routes.profile_routes import route as profile_route
from Backend.routes.registrer_routers import route as registrer_route
from fastapi.staticfiles import StaticFiles
import os


app = FastAPI()



app.mount("/static", StaticFiles(directory="Frontend/static"), name="static")

app.include_router(login_route)
app.include_router(home_route)
app.include_router(cake_route)
app.include_router(profile_route)
app.include_router(products_route)
app.include_router(registrer_route)
app.include_router(auth_route, prefix="/auth", tags=["auth"])



