from fastapi import APIRouter, status, HTTPException
from database.schemas.worker import worker_schema,workers_schema
from database.models.worker import Worker
from database.client import db_client
from bson import ObjectId

# Iniciar entorno virtual: source myenv/bin/activate


router4= APIRouter(prefix="/worker",tags = ["worker"])


@router4.get("/", response_model=list[Worker])
async def workers():
    return workers_schema(db_client.workers.find())


# PATH
@router4.get("/{id}")
async def worker(id: str):
    return searchByField("_id",ObjectId(id))


# QUERY

@router4.get("/{field}/{key}")
async def searchByAttribute(field: str, key:str):
    if field == "id":
        field = "_id"
        key = ObjectId(key)
    return searchByField(field, key)

@router4.post("/", status_code=status.HTTP_201_CREATED, response_model=Worker)
async def worker(worker: Worker):
    if (type(searchByField("mail", worker.mail)) == Worker or
            type(searchByField("cedula", worker.cedula)) == Worker or
            type(searchByField("username", worker.username)) == Worker):
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Worker already exist (cedula, mail or username can be repeated)")
    worker_dict = dict(worker)
    del worker_dict["id"]
    id = db_client.workers.insert_one(worker_dict).inserted_id
    new_worker = worker_schema(db_client.workers.find_one({"_id":id}))
    return Worker(**new_worker)

@router4.put("/")
async def worker(worker:Worker):
    worker_dict = dict(worker)
    mail_cedula_username_verification(worker_dict["id"], worker_dict)
    del worker_dict["id"]
    try:
        db_client.workers.find_one_and_replace({"_id":ObjectId(worker.id)},worker_dict)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker doesn't exist")
    return searchByField("_id",ObjectId(worker.id))

@router4.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def worker(id: str):
    found = db_client.workers.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker doesn't exist")


def searchByField(field:str, key: str | ObjectId):
    try:
        worker = worker_schema(db_client.workers.find_one({field: key}))
        return Worker(**worker)
    except:
        return None

def mail_cedula_username_verification(id, put_worker_dict: dict):
    search = db_client.workers.find_one({"cedula": put_worker_dict["cedula"]})
    if search is not None:
        worker = worker_schema(search)
        if worker["id"] != id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Already exist a worker with this cedula")

    search = db_client.workers.find_one({"username": put_worker_dict["username"]})
    if search is not None:
        worker = worker_schema(search)
        if worker["id"] != id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Already exist a worker with this username")
    search = db_client.workers.find_one({"mail": put_worker_dict["mail"]})
    if search is not None:
        worker = worker_schema(search)
        if worker["id"] != id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Already exist a worker with this mail")


