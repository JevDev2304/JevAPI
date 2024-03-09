from fastapi import APIRouter, status, HTTPException
from database.schemas.report import report_schema, reports_schema
from database.models.report import Report
from house import house_exist
from database.client import db_client
from bson import ObjectId

# Iniciar entorno virtual: source myenv/bin/activate


router3 = APIRouter(prefix="/report", tags=["report"])


@router3.get("/", response_model=list[Report])
async def reports():
    return reports_schema(db_client.reports.find())


# PATH
@router3.get("/{id}")
async def report(id: str):
    return searchByField("_id", ObjectId(id))



@router3.get("/{field}/{key}")
async def searchByAttribute(field: str, key:str):
    if field == "id":
        field = "_id"
        key = ObjectId(key)
    return searchByField(field, key)
@router3.post("/", status_code=status.HTTP_201_CREATED, response_model=Report)
async def report(report: Report):
    house_exist(report.house_id)
    report_dict = dict(report)
    del report_dict["id"]
    id = db_client.reports.insert_one(report_dict).inserted_id
    new_report = report_schema(db_client.reports.find_one({"_id": id}))
    return Report(**new_report)


@router3.put("/")
async def report(report: Report):
    house_exist(report.house_id)
    report_dict = dict(report)
    del report_dict["id"]
    try:
        db_client.reports.find_one_and_replace({"_id": ObjectId(report.id)}, report_dict)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report doesn't exist")
    return searchByField("_id", ObjectId(report.id))


@router3.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def report(id: str):
    found = db_client.reports.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report doesn't exist")


def searchByField(field:str, key: str | ObjectId):
    try:
        reports = db_client.reports.find({field: key})
        return reports_schema(reports)
    except:
        return {"Error": "The leases doesn't exist "}
