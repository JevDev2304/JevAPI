from fastapi import APIRouter, status, HTTPException
from database.schemas.house import house_schema,houses_schema
from database.models.house import House
from database.client import db_client
from bson import ObjectId
from bson.errors import InvalidId

# Iniciar entorno virtual: source myenv/bin/activate
# Iniciar servidor: uvicorn users:app --reload




router2 = APIRouter(prefix="/house",tags = ["house"])


@router2.get("/", response_model=list[House])
async def houses():
    return houses_schema(db_client.houses.find())


# PATH
@router2.get("/{id}")
async def house(id: str):
    try:
        return searchByField("_id",ObjectId(id))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House doesn't exist")

@router2.get("/{field}/{key}")
async def searchByAttribute(field: str, key:str):
    if field == "id":
        field = "_id"
        key = ObjectId(key)
    return searchByField(field, key)


@router2.post("/", status_code=status.HTTP_201_CREATED, response_model=House)
async def house(house: House):
    if type(searchByField("address",house.address.replace(" ", ""))) == House:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="House already exist")
    else:
        house_dict = dict(house)
        house_dict["address"]= house_dict["address"].replace(" ","")
        del house_dict["id"]
        id = db_client.houses.insert_one(house_dict).inserted_id
        new_house= house_schema(db_client.houses.find_one({"_id": id}))
        return House(**new_house)


@router2.put("/")
async def house(house:House):
    house_exist(house.id)
    house_dict = dict(house)
    address_verification(house.id,house_dict)
    del house_dict["id"]
    house_dict["address"] = house_dict["address"].replace(" ","")
    db_client.houses.find_one_and_replace({"_id":ObjectId(house.id)},house_dict)
    return searchByField("_id",ObjectId(house.id))

@router2.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def house(id: str):
    found = db_client.houses.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House doesn't exist")



def searchByField(field:str, key: str | ObjectId):
    try:
        house= house_schema(db_client.houses.find_one({field: key}))
        return House(**house)
    except:
        return None


def houses_exist(houses: list):
    try:
        for house in houses:
            house_schema(db_client.houses.find_one({"_id": ObjectId(house)}))
    except:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Some of the owner's houses were not found")

def house_exist(house: str):
    try:
        house_schema(db_client.houses.find_one({"_id": ObjectId(house)}))
    except:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The house_id doesn't exist")

def address_verification(id, put_house_dict: dict):
    search = db_client.houses.find_one({"address": put_house_dict["address"].replace(" ", "")})
    if search is not None:
        house = house_schema(search)
        if house["id"] != id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Already exist a house with this address")