from fastapi import APIRouter, status, HTTPException
from database.schemas.lease import lease_schema, leases_schema
from database.models.lease import Lease
from database.client import db_client
from bson import ObjectId
from house import house_exist
from owner import owner_exist

# Iniciar entorno virtual: source myenv/bin/activate


router5 = APIRouter(prefix="/lease",tags = ["lease"])


@router5.get("/", response_model=list[Lease])
async def leases():
    return leases_schema(db_client.leases.find())


# PATH
@router5.get("/{id}")
async def lease(id: str):
    return searchByField("_id",ObjectId(id))




@router5.get("/{field}/{key}")
async def searchByAttribute(field: str, key:str):
    if field == "id":
        field = "_id"
        key = ObjectId(key)
    return searchByField(field, key)

@router5.post("/", status_code=status.HTTP_201_CREATED, response_model=Lease)
async def lease(lease: Lease):
    house_exist(lease.house_id)
    owner_exist(lease.owner_cedula)
    lease_dict = dict(lease)
    del lease_dict["id"]
    id = db_client.leases.insert_one(lease_dict).inserted_id
    new_lease = lease_schema(db_client.leases.find_one({"_id":id}))
    return Lease(**new_lease)

@router5.put("/")
async def owner(lease:Lease):
    lease_dict = dict(lease)
    del lease_dict["id"]
    try:
        db_client.leases.find_one_and_replace({"_id":ObjectId(lease.id)},lease_dict)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lease doesn't exist")
    return searchByField("_id",ObjectId(lease.id))

@router5.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def owner(id: str):
    found = db_client.leases.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lease doesn't exist")


def searchByField(field:str, key: str | ObjectId):
    try:
        leases = db_client.leases.find({field: key})
        return leases_schema(leases)
    except:
        return {"Error": "The leases doesn't exist "}


