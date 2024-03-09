from fastapi import APIRouter, status, HTTPException
from database.schemas.owner import owner_schema, owners_schema
from database.models.owner import Owner
from house import houses_exist
from database.client import db_client
from bson import ObjectId

# Iniciar entorno virtual: source myenv/bin/activate


router = APIRouter(prefix="/owner", tags=["owner"])


@router.get("/", response_model=list[Owner])
async def owners():
    return owners_schema(db_client.owners.find())


# PATH
@router.get("/{id}")
async def owner(id: str):
    return searchByField("_id", ObjectId(id))



@router.get("/{field}/{key}")
async def searchByAttribute(field: str, key:str):
    if field == "id":
        field = "_id"
        key = ObjectId(key)
    return searchByField(field, key)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Owner)
async def owner(owner: Owner):
    if (type(searchByField("mail", owner.mail)) == Owner or
            type(searchByField("cedula", owner.cedula)) == Owner or
            type(searchByField("username", owner.username)) == Owner):

        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Owner already exist")
    else:
        houses_exist(list(owner.houses))
        owner_dict = dict(owner)
        del owner_dict["id"]
        id = db_client.owners.insert_one(owner_dict).inserted_id
        new_owner = owner_schema(db_client.owners.find_one({"_id": id}))
        return Owner(**new_owner)


@router.put("/")
async def owner(owner: Owner):
    houses_exist(list(owner.houses))
    owner_dict = dict(owner)
    mail_cedula_username_verification(owner_dict["id"], owner_dict)
    del owner_dict["id"]
    try:
        db_client.owners.find_one_and_replace({"_id": ObjectId(owner.id)}, owner_dict)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner doesn't exist")
    return searchByField("_id", ObjectId(owner.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def owner(id: str):
    found = db_client.owners.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner doesn't exist")


def searchByField(field: str, key: str | ObjectId):
    try:
        owner = owner_schema(db_client.owners.find_one({field: key}))
        return Owner(**owner)
    except:
        return {"Error": "The owner doesn't exist "}

def owner_exist(owner_cedula: str):
    try:
        owner_schema(db_client.owners.find_one({"cedula":owner_cedula}))
    except:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The owner_cedula doesn't exist")
def mail_cedula_username_verification(id, put_owner_dict: dict):
    search = db_client.owners.find_one({"cedula": put_owner_dict["cedula"]})
    if search is not None:
        owner = owner_schema(search)
        if owner["id"] != id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Already exist an owner with this cedula")

    search = db_client.owners.find_one({"username": put_owner_dict["username"]})
    if search is not None:
        owner = owner_schema(search)
        if owner["id"] != id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Already exist an owner with this username")
    search = db_client.owners.find_one({"mail": put_owner_dict["mail"]})
    if search is not None:
        owner = owner_schema(search)
        if owner["id"] != id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Already exist an owner with this mail")
