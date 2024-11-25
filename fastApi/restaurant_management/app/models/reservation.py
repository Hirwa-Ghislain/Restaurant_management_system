# app/models/reservation.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from ..database import Base
from datetime import datetime

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    party_size = Column(Integer)
    reservation_time = Column(DateTime)
    contact_number = Column(String)
    is_confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)