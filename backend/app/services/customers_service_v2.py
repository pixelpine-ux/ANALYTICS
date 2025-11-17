from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any, Optional
from ..models.analytics import Customer
from ..core.base_service import BaseService
from ..core.events import Event, EventType, event_bus
from fastapi import HTTPException

class CustomersService(BaseService[Customer]):
    def __init__(self, db: Session):
        super().__init__(Customer, db)
    
    async def create_customer(self, customer_data: Dict[str, Any]) -> Customer:
        """Create a new customer with event emission"""
        try:
            return await self.create(customer_data)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error creating customer: {str(e)}")
    
    async def update_customer(self, customer_id: str, customer_data: Dict[str, Any]) -> Optional[Customer]:
        """Update existing customer with event emission"""
        try:
            # For customers, ID is string-based
            customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
            if not customer:
                return None
            
            for field, value in customer_data.items():
                setattr(customer, field, value)
            
            self.db.commit()
            self.db.refresh(customer)
            
            await self._emit_updated_event(customer)
            return customer
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error updating customer: {str(e)}")
    
    async def delete_customer(self, customer_id: str) -> bool:
        """Delete customer with event emission"""
        try:
            customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
            if not customer:
                return False
            
            await self._emit_deleted_event(customer)
            self.db.delete(customer)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error deleting customer: {str(e)}")
    
    # Event emission methods
    async def _emit_created_event(self, customer: Customer):
        event = Event(
            event_type=EventType.CUSTOMER_CREATED,
            entity_id=str(customer.id),
            entity_type="customer",
            data=self._obj_to_dict(customer),
            timestamp=datetime.utcnow()
        )
        await event_bus.publish(event)
    
    async def _emit_updated_event(self, customer: Customer):
        event = Event(
            event_type=EventType.CUSTOMER_UPDATED,
            entity_id=str(customer.id),
            entity_type="customer",
            data=self._obj_to_dict(customer),
            timestamp=datetime.utcnow()
        )
        await event_bus.publish(event)
    
    async def _emit_deleted_event(self, customer: Customer):
        event = Event(
            event_type=EventType.CUSTOMER_UPDATED,
            entity_id=str(customer.id),
            entity_type="customer",
            data=self._obj_to_dict(customer),
            timestamp=datetime.utcnow()
        )
        await event_bus.publish(event)