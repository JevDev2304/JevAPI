from fastapi import FastAPI
from routers import products, users,jwt_auth_users
from usersMongoDb import router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(router)



#Including static resources
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return "Hola FastApi"

@app.get("/url")
async def url():
    return {"url_curso": "https://mouredev.com/python"}