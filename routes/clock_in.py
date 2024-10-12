from typing import Optional
from fastapi import APIRouter, HTTPException, status
from bson.objectid import ObjectId
from datetime import datetime, date
from models import ClockInCreate, ClockInUpdate
from database import clock_in_collection, item_helper

router = APIRouter()

# Helper function to convert `date` to `datetime`
def convert_date_to_datetime(data: dict):
    for key, value in data.items():
        if isinstance(value, date):  
            data[key] = datetime.combine(value, datetime.min.time()) 
    return data

# POST /clock-in - Create clock-in record
@router.post("/clock-in", status_code=status.HTTP_201_CREATED)
async def create_clock_in(record: ClockInCreate):
    record_data = record.dict()
    record_data['insert_datetime'] = datetime.utcnow()

    record_data = convert_date_to_datetime(record_data)

    result = await clock_in_collection.insert_one(record_data)
    created_record = await clock_in_collection.find_one({"_id": result.inserted_id})
    return item_helper(created_record)

# GET /clock-in/filter - Filter clock-in records
@router.get("/clock-in/filter")
async def filter_clock_ins(email: Optional[str] = None, location: Optional[str] = None, insert_datetime: Optional[datetime] = None):
    query = {}
    if email:
        query['email'] = email
    if location:
        query['location'] = location
    if insert_datetime:
        query['insert_datetime'] = {"$gte": insert_datetime}
    
    records = await clock_in_collection.find(query).to_list(length=100)
    return [item_helper(record) for record in records]

# DELETE /clock-in/{id} - Delete clock-in record by ID
@router.delete("/clock-in/{id}")
async def delete_clock_in(id: str):
    result = await clock_in_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted successfully"}

# PUT /clock-in/{id} - Update clock-in record
@router.put("/clock-in/{id}")
async def update_clock_in(id: str, record: ClockInUpdate):
    record_data = {k: v for k, v in record.dict().items() if v is not None}

    record_data = convert_date_to_datetime(record_data)

    result = await clock_in_collection.update_one({"_id": ObjectId(id)}, {"$set": record_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    
    updated_record = await clock_in_collection.find_one({"_id": ObjectId(id)})
    return item_helper(updated_record)
