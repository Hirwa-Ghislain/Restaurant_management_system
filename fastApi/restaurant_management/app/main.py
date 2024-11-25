# app/main.py
from fastapi import FastAPI
from .routers import orders, reservations, feedback
from .database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Restaurant Management System")

# Include routers
app.include_router(orders.router)
app.include_router(reservations.router)
app.include_router(feedback.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Restaurant Management System API"}