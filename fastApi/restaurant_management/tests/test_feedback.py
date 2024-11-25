
# tests/test_feedback.py
import pytest
from fastapi.testclient import TestClient
from ..database import Base, get_db
from ..main import app

def test_create_feedback(client):
    response = client.post(
        "/feedback/",
        json={
            "customer_name": "Test Customer",
            "rating": 4.5,
            "comment": "Great service!"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "Test Customer"
    assert data["rating"] == 4.5
    assert "id" in data