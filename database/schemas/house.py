def house_schema(house) -> dict:
    return {"id":str(house["_id"]),
            "address": str(house["address"]),
            "description": house["description"],
            "image": house["image"]
            }

def houses_schema(houses) -> list:
    return [house_schema(house) for house in houses]

