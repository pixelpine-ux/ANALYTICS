from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any, Optional, List
from ..models.analytics import Expense
from ..core.base_service import BaseService
from ..core.events import Event, EventType, event_bus
from fastapi import HTTPException

class ExpensesService(BaseService[Expense]):
    def __init__(self, db: Session):
        super().__init__(Expense, db)
    
    async def create_expense(self, expense_data: Dict[str, Any]) -> Expense:
        """Create a new expense with event emission"""
        try:
            # Convert amount to cents if provided as float
            if 'amount' in expense_data:
                expense_data['amount_cents'] = int(expense_data.pop('amount') * 100)
            
            return await self.create(expense_data)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error creating expense: {str(e)}")
    
    def get_expenses(self, skip: int = 0, limit: int = 100, 
                    start_date: Optional[datetime] = None,
                    end_date: Optional[datetime] = None) -> List[Expense]:
        """Get expenses with optional date filtering"""
        query = self.db.query(Expense)
        
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
            
        return query.offset(skip).limit(limit).all()
    
    async def update_expense(self, expense_id: int, expense_data: Dict[str, Any]) -> Optional[Expense]:
        """Update existing expense with event emission"""
        try:
            # Convert amount to cents if provided as float
            if 'amount' in expense_data:
                expense_data['amount_cents'] = int(expense_data.pop('amount') * 100)
            
            return await self.update(expense_id, expense_data)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error updating expense: {str(e)}")
    
    async def delete_expense(self, expense_id: int) -> bool:
        """Delete expense with event emission"""
        try:
            return await self.delete(expense_id)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error deleting expense: {str(e)}")
    
    # Event emission methods
    async def _emit_created_event(self, expense: Expense):
        event = Event(
            event_type=EventType.EXPENSE_CREATED,
            entity_id=str(expense.id),
            entity_type="expense",
            data=self._obj_to_dict(expense),
            timestamp=datetime.utcnow()
        )
        await event_bus.publish(event)
    
    async def _emit_updated_event(self, expense: Expense):
        event = Event(
            event_type=EventType.EXPENSE_UPDATED,
            entity_id=str(expense.id),
            entity_type="expense",
            data=self._obj_to_dict(expense),
            timestamp=datetime.utcnow()
        )
        await event_bus.publish(event)
    
    async def _emit_deleted_event(self, expense: Expense):
        event = Event(
            event_type=EventType.EXPENSE_UPDATED,
            entity_id=str(expense.id),
            entity_type="expense",
            data=self._obj_to_dict(expense),
            timestamp=datetime.utcnow()
        )
        await event_bus.publish(event)