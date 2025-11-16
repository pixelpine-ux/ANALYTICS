from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..core.database import get_db
from ..models.schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from ..services.expenses_service import ExpensesService

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    """Create a new expense record"""
    service = ExpensesService(db)
    db_expense = service.create_expense(expense)
    # Convert cents back to dollars for response
    return ExpenseResponse(
        id=db_expense.id,
        date=db_expense.date,
        description=db_expense.description,
        amount=db_expense.amount_cents / 100,
        category=db_expense.category,
        created_at=db_expense.created_at
    )

@router.get("/", response_model=List[ExpenseResponse])
def get_expenses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get expenses with optional pagination and date filtering"""
    service = ExpensesService(db)
    expenses = service.get_expenses(skip=skip, limit=limit, start_date=start_date, end_date=end_date)
    return [
        ExpenseResponse(
            id=expense.id,
            date=expense.date,
            description=expense.description,
            amount=expense.amount_cents / 100,
            category=expense.category,
            created_at=expense.created_at
        )
        for expense in expenses
    ]

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    """Get a specific expense by ID"""
    service = ExpensesService(db)
    expense = service.get_expense(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return ExpenseResponse(
        id=expense.id,
        date=expense.date,
        description=expense.description,
        amount=expense.amount_cents / 100,
        category=expense.category,
        created_at=expense.created_at
    )

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense_update: ExpenseUpdate, db: Session = Depends(get_db)):
    """Update an existing expense"""
    service = ExpensesService(db)
    expense = service.update_expense(expense_id, expense_update)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return ExpenseResponse(
        id=expense.id,
        date=expense.date,
        description=expense.description,
        amount=expense.amount_cents / 100,
        category=expense.category,
        created_at=expense.created_at
    )

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """Delete an expense"""
    service = ExpensesService(db)
    success = service.delete_expense(expense_id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return {"message": "Expense deleted successfully"}

@router.get("/by-category/", response_model=dict)
def get_expenses_by_category(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db)
):
    """Get expense totals grouped by category for a date range"""
    service = ExpensesService(db)
    return service.get_expenses_by_category(start_date, end_date)