# app/schemas/order.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrderBase(BaseModel):
    customer_name: str
    items: str
    total_amount: float
    status: str = "pending"

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True