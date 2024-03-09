from pydantic import BaseModel


class Worker(BaseModel):
    id: str | None
    cedula: str
    username: str
    name : str
    mail: str
    password: str


