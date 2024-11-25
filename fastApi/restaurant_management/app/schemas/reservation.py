# app/schemas/reservation.py
from pydantic import BaseModel
from datetime import datetime

class ReservationBase(BaseModel):
    customer_name: str
    party_size: int
    reservation_time: datetime
    contact_number: str

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    is_confirmed: bool
    created_at: datetime

    class Config:
        from_attributes = True