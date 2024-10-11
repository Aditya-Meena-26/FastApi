from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from bson.objectid import ObjectId
from models import ItemCreate, ItemUpdate
from database import items_collection, item_helper
from datetime import date, datetime

router = APIRouter()

# Helper function to convert `date` to `datetime`
def convert_date_to_datetime(data: dict):
    for key, value in data.items():
        if isinstance(value, date):  # Check if the value is a `date`
            data[key] = datetime.combine(value, datetime.min.time())  # Convert to `datetime`
    return data

# POST /items - Create new item
@router.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    item_data = item.dict()
    item_data['insert_date'] = datetime.utcnow()  # Automatically insert date

    # Convert any `date` fields to `datetime`
    item_data = convert_date_to_datetime(item_data)

    result = await items_collection.insert_one(item_data)
    created_item = await items_collection.find_one({"_id": result.inserted_id})
    return item_helper(created_item)

# GET /items/filter - Filter items
@router.get("/items/filter")
async def filter_items(email: Optional[str] = None, expiry_date: Optional[date] = None, insert_date: Optional[date] = None, quantity: Optional[int] = None):
    query = {}
    if email:
        query['email'] = email
    if expiry_date:
        query['expiry_date'] = {"$gte": expiry_date}
    if insert_date:
        query['insert_date'] = {"$gte": insert_date}
    if quantity:
        query['quantity'] = {"$gte": quantity}

    items = await items_collection.find(query).to_list(length=100)
    return [item_helper(item) for item in items]

# MongoDB Aggregation - Get count of items for each email
@router.get("/items/aggregation")
async def aggregate_items():
    aggregation = [
        {"$group": {"_id": "$email", "count": {"$sum": 1}}}
    ]
    results = await items_collection.aggregate(aggregation).to_list(length=100)
    return results

# DELETE /items/{id} - Delete item by ID
@router.delete("/items/{id}")
async def delete_item(id: str):
    result = await items_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

# PUT /items/{id} - Update item details
@router.put("/items/{id}")
async def update_item(id: str, item: ItemUpdate):
    item_data = {k: v for k, v in item.dict().items() if v is not None}

    # Convert any `date` fields to `datetime`
    item_data = convert_date_to_datetime(item_data)

    result = await items_collection.update_one({"_id": ObjectId(id)}, {"$set": item_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item = await items_collection.find_one({"_id": ObjectId(id)})
    return item_helper(updated_item)
