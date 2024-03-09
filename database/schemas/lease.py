def lease_schema(lease) -> dict:
    return {"id":str(lease["_id"]),
            "start_date": str(lease["start_date"]),
            "final_date" : str(lease["final_date"]),
            "house_id": str(lease["house_id"]),
            "tenant_name": str(lease["tenant_name"]),
            "tenant_cedula": str(lease["tenant_cedula"]),
            "owner_cedula": str(lease["owner_cedula"]),
            "video": str(lease["video"]),
            "signature": str(lease["signature"])
            }



def leases_schema(leases) -> list:
    return [lease_schema(lease) for lease in leases]



