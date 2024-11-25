# app/models/feedback.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from ..database import Base
from datetime import datetime

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    rating = Column(Float)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)