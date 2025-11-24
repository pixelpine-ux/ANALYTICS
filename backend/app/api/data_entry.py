from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator

from ..core.database import get_db
from ..services.sales_service import SalesService
from ..services.customers_service_v2 import CustomersService
from ..services.expenses_service_v2 import ExpensesService

router = APIRouter(prefix="/entry", tags=["Data Entry"])

# Simple data models for manual entry
class QuickSale(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=200)
    amount: float = Field(..., gt=0, description="Amount in dollars")
    customer_id: Optional[str] = Field(None, max_length=50)
    category: Optional[str] = Field(None, max_length=100)
    date: Optional[datetime] = None
    
    @validator('product_name')
    def validate_product_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Product name cannot be empty')
        return v.strip()
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        if v > 999999.99:
            raise ValueError('Amount too large')
        return round(v, 2)

class QuickCustomer(BaseModel):
    id: str
    name: str
    email: str = None

class QuickExpense(BaseModel):
    description: str
    amount: float
    category: str = None
    date: datetime = None

@router.post("/quick-sale")
async def create_quick_sale(
    sale: QuickSale,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Quick sale entry for manual data input"""
    sales_service = SalesService(db)
    
    sale_data = {
        "product_name": sale.product_name,
        "amount": sale.amount,
        "customer_id": sale.customer_id,
        "category": sale.category,
        "date": sale.date or datetime.utcnow()
    }
    
    try:
        db_sale = await sales_service.create_sale(sale_data)
        return {
            "success": True,
            "sale_id": db_sale.id,
            "message": "Sale recorded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/quick-customer")
async def create_quick_customer(
    customer: QuickCustomer,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Quick customer entry for manual data input"""
    customers_service = CustomersService(db)
    
    customer_data = {
        "id": customer.id,
        "name": customer.name,
        "email": customer.email
    }
    
    try:
        db_customer = await customers_service.create_customer(customer_data)
        return {
            "success": True,
            "customer_id": db_customer.id,
            "message": "Customer created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/quick-expense")
async def create_quick_expense(
    expense: QuickExpense,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Quick expense entry for manual data input"""
    expenses_service = ExpensesService(db)
    
    expense_data = {
        "description": expense.description,
        "amount": expense.amount,
        "category": expense.category,
        "date": expense.date or datetime.utcnow()
    }
    
    try:
        db_expense = await expenses_service.create_expense(expense_data)
        return {
            "success": True,
            "expense_id": db_expense.id,
            "message": "Expense recorded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/suggestions/products")
def get_product_suggestions(
    query: str = "",
    db: Session = Depends(get_db)
):
    """Get product name suggestions for autocomplete"""
    from sqlalchemy import func
    from ..models.analytics import Sale
    
    results = db.query(Sale.product_name).filter(
        Sale.product_name.ilike(f"%{query}%")
    ).group_by(Sale.product_name).limit(10).all()
    
    return [result.product_name for result in results]

@router.get("/suggestions/customers")
def get_customer_suggestions(
    query: str = "",
    db: Session = Depends(get_db)
):
    """Get customer suggestions for autocomplete"""
    from ..models.analytics import Customer
    
    results = db.query(Customer.id, Customer.name).filter(
        Customer.name.ilike(f"%{query}%")
    ).limit(10).all()
    
    return [
        {"id": result.id, "name": result.name}
        for result in results
    ]