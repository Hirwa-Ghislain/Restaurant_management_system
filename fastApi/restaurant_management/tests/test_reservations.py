# tests/test_reservations.py
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from ..database import Base, get_db
from ..main import app

def test_create_reservation(client):
    response = client.post(
        "/reservations/",
        json={
            "customer_name": "Test Customer",
            "party_size": 4,
            "reservation_time": datetime.utcnow().isoformat(),
            "contact_number": "123-456-7890"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "Test Customer"
    assert data["party_size"] == 4
    assert "id" in data