from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import List, Optional, Dict, Any
from ..models.analytics import Sale
from ..core.base_service import BaseService
from ..core.events import Event, EventType, event_bus
from fastapi import HTTPException

class SalesService(BaseService[Sale]):
    def __init__(self, db: Session):
        super().__init__(Sale, db)
    
    async def create_sale(self, sale_data: Dict[str, Any]) -> Sale:
        """Create a new sale record with event emission"""
        try:
            # Convert amount to cents if provided as float
            if 'amount' in sale_data:
                sale_data['amount_cents'] = int(sale_data.pop('amount') * 100)
            
            return await self.create(sale_data)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error creating sale: {str(e)}")
    
    def get_sales(self, skip: int = 0, limit: int = 100, 
                  start_date: Optional[datetime] = None,
                  end_date: Optional[datetime] = None) -> List[Sale]:
        """Get sales with optional date filtering"""
        query = self.db.query(Sale)
        
        if start_date:
            query = query.filter(Sale.date >= start_date)
        if end_date:
            query = query.filter(Sale.date <= end_date)
            
        return query.order_by(desc(Sale.date)).offset(skip).limit(limit).all()
    
    async def update_sale(self, sale_id: int, sale_data: Dict[str, Any]) -> Optional[Sale]:
        """Update existing sale with event emission"""
        try:
            # Convert amount to cents if provided as float
            if 'amount' in sale_data:
                sale_data['amount_cents'] = int(sale_data.pop('amount') * 100)
            
            return await self.update(sale_id, sale_data)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error updating sale: {str(e)}")
    
    async def delete_sale(self, sale_id: int) -> bool:
        """Delete sale with event emission"""
        try:
            return await self.delete(sale_id)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error deleting sale: {str(e)}")
    
    # Event emission methods
    async def _emit_created_event(self, sale: Sale):
        event = Event(
            event_type=EventType.SALE_CREATED,
            entity_id=str(sale.id),
            entity_type="sale",
            data=self._obj_to_dict(sale),
            timestamp=datetime.utcnow()
        )
        await event_bus.publish(event)
    
    async def _emit_updated_event(self, sale: Sale):
        event = Event(
            event_type=EventType.SALE_UPDATED,
            entity_id=str(sale.id),
            entity_type="sale",
            data=self._obj_to_dict(sale),
            timestamp=datetime.utcnow()
        )
        await event_bus.publish(event)
    
    async def _emit_deleted_event(self, sale: Sale):
        event = Event(
            event_type=EventType.SALE_DELETED,
            entity_id=str(sale.id),
            entity_type="sale",
            data=self._obj_to_dict(sale),
            timestamp=datetime.utcnow()
        )
        await event_bus.publish(event)