from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


# Iniciar entorno virtual: source myenv/bin/activate
# Iniciar servidor: uvicorn users:app --reload

class User(BaseModel):
    id: int
    name: str
    mail: str
    password: str


class Error(BaseModel):
    error: str


users_list = [User(id=1, name="Juan", mail="juanesplatzi2304@gmail.com", password="1234"),
              User(id=2, name="Cristian", mail="cristian@gmail.com", password="2345"),
              User(id=3, name="Juanfer", mail="juanfe@gmail.com", password="3456")]
router = APIRouter(responses={404: {"message": "No encontrado"} },
                   tags = ["users"])


@router.get("/users")
async def users():
    return users_list


# PATH
@router.get("/user/{id}")
async def userjson(id: int):
    return searchUser(id)


# QUERY
@router.get("/userquery/")
async def userjson(id: int):
    return searchUser(id)


@router.post("/user/", status_code=201, response_model=User)
async def userjson(user: User):
    if type(searchUser(user.id)) == User:
        raise HTTPException(status_code=404, detail="User already exist ")
    else:
        users_list.append(user)
        return user


@router.put("/user/")
async def userjson(user: User):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            return user
    return Error(error="User to update not found")


@router.delete("/user/{id}")
async def userjson(id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            return saved_user
    return Error(error="User to delete not found")


def searchUser(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return Error(error="User not found")
