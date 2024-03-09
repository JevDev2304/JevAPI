from pydantic import BaseModel

class Owner(BaseModel):
    id: str | None
    cedula: str
    name : str
    username: str
    mail: str
    password: str
    houses: list[str]

