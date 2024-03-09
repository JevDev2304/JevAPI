from pydantic import BaseModel
class House(BaseModel):
    id: str | None
    address: str
    description: str
    image: str

