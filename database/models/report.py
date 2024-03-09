from pydantic import BaseModel


class Report(BaseModel):
    id: str | None
    contractor_name: str
    contractor_cedula: str
    house_id:  str
    description: str
    date: str


