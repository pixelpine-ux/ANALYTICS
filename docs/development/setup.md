# Development Setup Guide

## Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL (optional, SQLite for development)

## Backend Setup

### 1. Environment Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Initialize database
alembic upgrade head

# Or create fresh database
python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### 3. Environment Variables
```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Start Development Server
```bash
uvicorn app.main:app --reload
```

### 5. Verify Installation
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Frontend Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

### 3. Verify Installation
- Frontend: http://localhost:5173

## Testing Setup

### 1. Run Backend Tests
```bash
cd backend
pytest tests/ -v
```

### 2. Test Event System
```bash
python app/test_events.py
```

## API Testing
Use the interactive documentation at http://localhost:8000/docs to test all endpoints.