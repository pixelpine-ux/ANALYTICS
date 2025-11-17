# Backend Test Suite

## Overview
Comprehensive test suite for the retail analytics backend system covering all components and integration scenarios.

## Test Structure

### Core Tests
- **test_events.py** - Event system functionality
- **test_services.py** - Service layer tests (Sales, Customers, KPI)
- **test_api.py** - API endpoint tests
- **test_csv_upload.py** - CSV upload functionality
- **test_integration.py** - End-to-end integration tests

### Test Configuration
- **conftest.py** - Pytest configuration and fixtures
- **README.md** - This documentation

## Running Tests

### All Tests
```bash
cd backend
pytest tests/ -v
```

### Specific Test Files
```bash
pytest tests/test_events.py -v
pytest tests/test_services.py -v
pytest tests/test_api.py -v
```

### Coverage Report
```bash
pytest tests/ --cov=app --cov-report=html
```

### Test Categories

#### Unit Tests
- Event system components
- Service layer methods
- Data validation
- KPI calculations

#### API Tests
- Endpoint functionality
- Request/response validation
- Error handling
- Authentication (future)

#### Integration Tests
- Event-driven workflows
- Data consistency across APIs
- End-to-end user scenarios
- CSV upload to analytics flow

## Test Data
Tests use SQLite in-memory database for isolation and speed.

## Fixtures Available
- `db_session` - Database session for tests
- `client` - FastAPI test client
- Automatic database cleanup between tests

## Test Coverage Goals
- **Unit Tests**: 90%+ coverage
- **API Tests**: All endpoints covered
- **Integration**: Key user workflows tested
- **Error Handling**: All error scenarios covered