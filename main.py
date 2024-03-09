from fastapi import FastAPI
from owner import router
from house import router2
from report import router3
from worker import router4
from lease import router5
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(router)
app.include_router(router2)
app.include_router(router3)
app.include_router(router4)
app.include_router(router5)


#Including static resources
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def greeting():
    return {"Message": """Welcome to JevAPI, This API is made for a rent houses inventory. Made by JevDev2304 You can see the docs in /docs"""}

