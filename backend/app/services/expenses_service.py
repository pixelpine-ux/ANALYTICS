from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import List, Optional
from ..models.analytics import Expense
from ..models.schemas import ExpenseCreate, ExpenseUpdate
from fastapi import HTTPException

class ExpensesService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_expense(self, expense_data: ExpenseCreate) -> Expense:
        """Create a new expense record"""
        try:
            expense = Expense(
                date=expense_data.date,
                description=expense_data.description,
                amount_cents=int(expense_data.amount * 100),
                category=expense_data.category
            )
            self.db.add(expense)
            self.db.commit()
            self.db.refresh(expense)
            return expense
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error creating expense: {str(e)}")
    
    def get_expense(self, expense_id: int) -> Optional[Expense]:
        """Get expense by ID"""
        return self.db.query(Expense).filter(Expense.id == expense_id).first()
    
    def get_expenses(self, skip: int = 0, limit: int = 100,
                    start_date: Optional[datetime] = None,
                    end_date: Optional[datetime] = None) -> List[Expense]:
        """Get expenses with optional date filtering"""
        query = self.db.query(Expense)
        
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
            
        return query.order_by(desc(Expense.date)).offset(skip).limit(limit).all()
    
    def update_expense(self, expense_id: int, expense_data: ExpenseUpdate) -> Optional[Expense]:
        """Update existing expense"""
        try:
            expense = self.get_expense(expense_id)
            if not expense:
                return None
            
            update_data = expense_data.dict(exclude_unset=True)
            if 'amount' in update_data:
                update_data['amount_cents'] = int(update_data.pop('amount') * 100)
            
            for field, value in update_data.items():
                setattr(expense, field, value)
            
            self.db.commit()
            self.db.refresh(expense)
            return expense
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error updating expense: {str(e)}")
    
    def delete_expense(self, expense_id: int) -> bool:
        """Delete expense by ID"""
        try:
            expense = self.get_expense(expense_id)
            if not expense:
                return False
            
            self.db.delete(expense)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error deleting expense: {str(e)}")
    
    def get_expenses_by_category(self, start_date: datetime, end_date: datetime) -> dict:
        """Get expense totals grouped by category"""
        from sqlalchemy import func
        
        results = self.db.query(
            Expense.category,
            func.sum(Expense.amount_cents).label('total_cents')
        ).filter(
            Expense.date >= start_date,
            Expense.date <= end_date
        ).group_by(Expense.category).all()
        
        return {
            category or 'Uncategorized': total_cents / 100 
            for category, total_cents in results
        }
