from typing import Dict, Any, List, Callable
from datetime import datetime
from enum import Enum
import asyncio
import json
from dataclasses import dataclass, asdict

class EventType(Enum):
    # Sales events
    SALE_CREATED = "sale.created"
    SALE_UPDATED = "sale.updated"
    SALE_DELETED = "sale.deleted"
    
    # Customer events
    CUSTOMER_CREATED = "customer.created"
    CUSTOMER_UPDATED = "customer.updated"
    
    # Expense events
    EXPENSE_CREATED = "expense.created"
    EXPENSE_UPDATED = "expense.updated"
    
    # Analytics events
    KPI_CALCULATED = "kpi.calculated"
    REPORT_GENERATED = "report.generated"
    
    # Data sync events (for future POS integration)
    DATA_SYNC_REQUESTED = "data.sync.requested"
    DATA_SYNC_COMPLETED = "data.sync.completed"

@dataclass
class Event:
    event_type: EventType
    entity_id: str
    entity_type: str
    data: Dict[str, Any]
    timestamp: datetime
    source: str = "analytics"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type.value,
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source
        }

class EventBus:
    def __init__(self):
        self._handlers: Dict[EventType, List[Callable]] = {}
        self._event_store: List[Event] = []
    
    def subscribe(self, event_type: EventType, handler: Callable):
        """Subscribe a handler to an event type"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    async def publish(self, event: Event):
        """Publish an event to all subscribers"""
        # Store event for audit trail
        self._event_store.append(event)
        
        # Notify handlers
        if event.event_type in self._handlers:
            for handler in self._handlers[event.event_type]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)
                except Exception as e:
                    print(f"Error in event handler: {e}")
    
    def get_events(self, entity_id: str = None, event_type: EventType = None) -> List[Event]:
        """Get events from store with optional filtering"""
        events = self._event_store
        
        if entity_id:
            events = [e for e in events if e.entity_id == entity_id]
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        return events

# Global event bus instance
event_bus = EventBus()