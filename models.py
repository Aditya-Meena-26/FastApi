from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime

# Item Schema
class ItemCreate(BaseModel):
    name: str
    email: EmailStr
    item_name: str
    quantity: int
    expiry_date: date

class ItemUpdate(BaseModel):
    name: Optional[str]
    item_name: Optional[str]
    quantity: Optional[int]
    expiry_date: Optional[date]

# Clock-In Schema
class ClockInCreate(BaseModel):
    email: EmailStr
    location: str

class ClockInUpdate(BaseModel):
    location: Optional[str]

