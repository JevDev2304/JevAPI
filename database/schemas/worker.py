def worker_schema(worker) -> dict:
    return {"id":str(worker["_id"]),
            "cedula": str(worker["cedula"]),
            "username" : str(worker["username"]),
            "name": str(worker["name"]),
            "mail": str(worker["mail"]),
            "password": str(worker["password"])
            }

def workers_schema(workers) -> list:
    return [worker_schema(worker) for worker in workers]

