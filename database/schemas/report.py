def report_schema(report) -> dict:
    return {"id":str(report["_id"]),
            "contractor_name": str(report["contractor_name"]),
            "contractor_cedula" : str(report["contractor_cedula"]),
            "house_id": str(report["house_id"]),
            "description": str(report["description"]),
            "date": str(report["date"])
            }

def reports_schema(reports) -> list:
    return [report_schema(report) for report in reports]

