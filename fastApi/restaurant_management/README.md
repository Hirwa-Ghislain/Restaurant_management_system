# README.md
# Restaurant Management System

A FastAPI-based backend system for managing restaurant orders, reservations, and customer feedback.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

4. Access the API documentation at http://localhost:8000/docs

## Features

- Order Management
- Reservation System
- Customer Feedback
- API Documentation with Swagger UI
- SQLite Database (can be changed to PostgreSQL)

## Testing

Run tests with:
```bash
pytest
```

## API Endpoints

- Orders:
  - POST /orders/
  - GET /orders/
  - GET /orders/{order_id}
  - PUT /orders/{order_id}

- Reservations:
  - POST /reservations/
  - GET /reservations/
  - GET /reservations/{reservation_id}

- Feedback:
  - POST /feedback/
  - GET /feedback/