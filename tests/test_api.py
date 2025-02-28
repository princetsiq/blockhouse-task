import pytest
from fastapi.testclient import TestClient
from main import app  
from sqlmodel import Session
from main import get_session

client = TestClient(app)

# Dependency override to use an in-memory SQLite database for tests
@pytest.fixture(scope="function")
def test_db():
    """Creates a new database session for testing"""
    with Session(get_session()) as session:
        yield session


# Test Creating Orders
def test_create_valid_order():
    """Test that a valid order is created successfully"""
    response = client.post("/orders", json={
        "symbol": "AAPL",
        "quantity": 10,
        "price": 150.0,
        "order_type": "buy"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["quantity"] == 10
    assert data["price"] == 150.0
    assert data["order_type"] == "buy"

def test_create_order_missing_fields():
    """Test that an order fails if required fields are missing"""
    response = client.post("/orders", json={
        "symbol": "TSLA",
        "quantity": 5
    })
    assert response.status_code == 422  # Unprocessable Entity (missing fields)


# Test Retrieving Orders
def test_get_orders_empty():
    """Test retrieving orders when no orders exist (should return an empty list)"""
    response = client.get("/orders")
    assert response.status_code == 200
    assert response.json() == []

def test_get_orders_after_creation():
    """Test retrieving orders after adding an order"""
    client.post("/orders", json={
        "symbol": "GOOGL",
        "quantity": 3,
        "price": 2800.0,
        "order_type": "buy"
    })
    response = client.get("/orders")
    assert response.status_code == 200
    orders = response.json()
    symbols = [o["symbol"] for o in orders]
    assert "GOOGL" in symbols


# Edge Cases: Invalid Inputs
def test_create_order_negative_quantity():
    """Test creating an order with a negative quantity"""
    response = client.post("/orders", json={
        "symbol": "AMZN",
        "quantity": -5,
        "price": 3300.0,
        "order_type": "sell"
    })
    assert response.status_code == 422  # Should fail validation

def test_create_order_invalid_order_type():
    """Test creating an order with an invalid order type"""
    response = client.post("/orders", json={
        "symbol": "NFLX",
        "quantity": 10,
        "price": 500.0,
        "order_type": "hold"  # Invalid order type
    })
    assert response.status_code == 422


# Edge Case: Duplicate Orders
def test_create_duplicate_order():
    """Test that duplicate orders are handled correctly"""
    order_data = {
        "symbol": "TSLA",
        "quantity": 15,
        "price": 1200.0,
        "order_type": "buy"
    }
    
    client.post("/orders", json=order_data)
    response = client.post("/orders", json=order_data)  # Try creating duplicate
    assert response.status_code == 200  # Ensure duplicates are allowed or handle them in business logic


# Test API Performance
@pytest.mark.timeout(2)  # Ensure the request completes in under 2 seconds
def test_api_response_time():
    """Ensure that retrieving orders is fast"""
    response = client.get("/orders")
    assert response.status_code == 200
