from pydantic import BaseModel



class Lease(BaseModel):
    id: str | None
    start_date: str
    final_date: str
    house_id : str
    tenant_name : str
    tenant_cedula : str
    owner_cedula:str
    video : str
    signature : str


