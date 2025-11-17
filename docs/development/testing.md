# Testing Guide

## Overview
Comprehensive testing strategy for the retail analytics backend system.

## Test Structure

### Test Categories
1. **Unit Tests** - Individual components
2. **Integration Tests** - Component interactions
3. **API Tests** - Endpoint functionality
4. **End-to-End Tests** - Complete workflows

### Test Files
- `test_events.py` - Event system tests
- `test_services.py` - Service layer tests
- `test_api.py` - API endpoint tests
- `test_csv_upload.py` - CSV functionality tests
- `test_integration.py` - Integration scenarios

## Running Tests

### Prerequisites
```bash
cd backend
pip install pytest pytest-asyncio
```

### All Tests
```bash
pytest tests/ -v
```

### Specific Test Categories
```bash
# Unit tests
pytest tests/test_events.py tests/test_services.py -v

# API tests
pytest tests/test_api.py -v

# Integration tests
pytest tests/test_integration.py -v
```

### With Coverage
```bash
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html
```

## Test Database
Tests use SQLite in-memory database for:
- **Isolation** - Each test gets fresh database
- **Speed** - No disk I/O overhead
- **Simplicity** - No setup/teardown required

## Writing Tests

### Test Structure
```python
import pytest
from app.services.sales_service import SalesService

class TestSalesService:
    
    @pytest.mark.asyncio
    async def test_create_sale(self, db_session):
        service = SalesService(db_session)
        # Test implementation
```

### Available Fixtures
- `db_session` - Database session
- `client` - FastAPI test client

### Async Tests
Use `@pytest.mark.asyncio` for async functions:
```python
@pytest.mark.asyncio
async def test_async_function(self, db_session):
    result = await some_async_function()
    assert result is not None
```

## Test Data
Create test data in tests:
```python
def test_with_data(self, db_session):
    # Create test sale
    sale = Sale(
        product_name="Test Product",
        amount_cents=9999,
        date=datetime.utcnow()
    )
    db_session.add(sale)
    db_session.commit()
    
    # Test logic here
```

## API Testing
Test API endpoints:
```python
def test_api_endpoint(self, client):
    response = client.get("/api/v1/dashboard/kpis")
    assert response.status_code == 200
    data = response.json()
    assert "revenue" in data
```

## Event Testing
Test event system:
```python
@pytest.mark.asyncio
async def test_event_emission(self, db_session):
    events = []
    
    async def event_handler(event):
        events.append(event)
    
    event_bus.subscribe(EventType.SALE_CREATED, event_handler)
    
    # Trigger event
    service = SalesService(db_session)
    await service.create_sale({"product_name": "Test", "amount": 10})
    
    assert len(events) == 1
```

## Continuous Integration
Tests run automatically on:
- Pull requests
- Main branch commits
- Release builds

## Coverage Goals
- **Overall**: 85%+
- **Services**: 90%+
- **APIs**: 100%
- **Critical paths**: 100%

## Performance Testing
For load testing:
```bash
# Install locust
pip install locust

# Run load tests
locust -f tests/load_tests.py --host=http://localhost:8000
```