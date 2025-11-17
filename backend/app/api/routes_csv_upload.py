from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..core.database import get_db
from ..services.csv_upload_service import CSVUploadService

router = APIRouter(prefix="/data", tags=["CSV Upload"])

@router.post("/upload-sales-csv")
async def upload_sales_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Upload sales data via CSV file
    
    Expected CSV columns:
    - date (required): Sale date in YYYY-MM-DD format
    - product_name (required): Name of the product
    - amount (required): Sale amount as decimal
    - customer_id (optional): Customer identifier
    - category (optional): Product category
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    csv_service = CSVUploadService(db)
    result = await csv_service.upload_sales_csv(file)
    
    return result

@router.post("/upload-customers-csv")
async def upload_customers_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Upload customer data via CSV file
    
    Expected CSV columns:
    - id (required): Unique customer identifier
    - name (required): Customer name
    - email (optional): Customer email
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    csv_service = CSVUploadService(db)
    result = await csv_service.upload_customers_csv(file)
    
    return result

@router.post("/upload-expenses-csv")
async def upload_expenses_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Upload expense data via CSV file
    
    Expected CSV columns:
    - date (required): Expense date in YYYY-MM-DD format
    - description (required): Expense description
    - amount (required): Expense amount as decimal
    - category (optional): Expense category
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    csv_service = CSVUploadService(db)
    result = await csv_service.upload_expenses_csv(file)
    
    return result

@router.get("/upload-template/{data_type}")
async def get_csv_template(data_type: str):
    """
    Get CSV template for different data types
    """
    templates = {
        "sales": {
            "columns": ["date", "product_name", "amount", "customer_id", "category"],
            "example": {
                "date": "2024-01-15",
                "product_name": "Widget A",
                "amount": "29.99",
                "customer_id": "CUST001",
                "category": "Electronics"
            }
        },
        "customers": {
            "columns": ["id", "name", "email"],
            "example": {
                "id": "CUST001",
                "name": "John Doe",
                "email": "john@example.com"
            }
        },
        "expenses": {
            "columns": ["date", "description", "amount", "category"],
            "example": {
                "date": "2024-01-15",
                "description": "Office supplies",
                "amount": "45.50",
                "category": "Operations"
            }
        }
    }
    
    if data_type not in templates:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return templates[data_type]