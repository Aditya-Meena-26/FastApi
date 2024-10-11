from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import HTTPException

# MongoDB Configuration
client = AsyncIOMotorClient("mongodb://localhost:27017")  # Replace with your MongoDB URI
db = client['fastapi_app']

# Helper function to convert MongoDB ObjectId to string
def item_helper(item) -> dict:
    item['_id'] = str(item['_id'])
    return item

# Get collection
items_collection = db.get_collection("items")
clock_in_collection = db.get_collection("clock_in_records")
