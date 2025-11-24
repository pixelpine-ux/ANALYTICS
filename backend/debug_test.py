import sys
sys.path.append('.')

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

sale_data = {
    "product_name": "Test Product",
    "amount": 99.99,
    "customer_id": "CUST001",
    "category": "Electronics"
}

response = client.post("/api/v1/entry/quick-sale", json=sale_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
