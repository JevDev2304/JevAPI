from pydantic import BaseModel

class User(BaseModel):
    id: str | None
    username: str
    mail: str
    password: str

