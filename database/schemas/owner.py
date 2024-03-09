def owner_schema(owner) -> dict:
    return {"id":str(owner["_id"]),
            "cedula": owner["cedula"],
            "name": owner["name"],
            "username": owner["username"],
            "mail": owner["mail"],
            "password": owner["password"],
            "houses": owner["houses"]
            }

def owners_schema(owners) -> list:
    return [owner_schema(owner) for owner in owners]
