# app/schemas/feedback.py
from pydantic import BaseModel
from datetime import datetime

class FeedbackBase(BaseModel):
    customer_name: str
    rating: float
    comment: str

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True