from fastapi import APIRouter, status, HTTPException
from database.schemas.user import user_schema, users_schema
from database.models.user import  User
from database.client import db_client
from bson import ObjectId

# Iniciar entorno virtual: source myenv/bin/activate
# Iniciar servidor: uvicorn users:app --reload




users_list = []

router = APIRouter(prefix="/userdb",tags = ["usersdb"])


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


# PATH
@router.get("/{id}")
async def userjson(id: str):
    return searchUserByField("_id",ObjectId(id))


# QUERY
@router.get("/query")
async def userjson(id: str):
    return searchUserByField("_id", ObjectId(id))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def userjson(user: User):
    if type(searchUserByField("mail",user.mail))== User:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="User already exist")
    else:

        user_dict = dict(user)
        del user_dict["id"]
        id = db_client.users.insert_one(user_dict).inserted_id
        new_user = user_schema(db_client.users.find_one({"_id":id}))
        return User(**new_user)

@router.put("/")
async def userjson(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    try:
        db_client.users.find_one_and_replace({"_id":ObjectId(user.id)},user_dict)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn´t exist")
    return searchUserByField("_id",ObjectId(user.id))

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def userjson(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")


def searchUserByField(field:str, key: str | ObjectId):
    try:
        user = user_schema(db_client.users.find_one({field: key}))
        return User(**user)
    except:
        return {"Error": "The user doesn't exist "}


