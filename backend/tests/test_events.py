import pytest
import asyncio
from datetime import datetime
from app.core.events import Event, EventType, EventBus

class TestEventSystem:
    
    def test_event_creation(self):
        """Test event object creation"""
        event = Event(
            event_type=EventType.SALE_CREATED,
            entity_id="123",
            entity_type="sale",
            data={"amount": 100},
            timestamp=datetime.utcnow()
        )
        
        assert event.event_type == EventType.SALE_CREATED
        assert event.entity_id == "123"
        assert event.entity_type == "sale"
        assert event.data["amount"] == 100
    
    def test_event_to_dict(self):
        """Test event serialization"""
        event = Event(
            event_type=EventType.SALE_CREATED,
            entity_id="123",
            entity_type="sale",
            data={"amount": 100},
            timestamp=datetime.utcnow()
        )
        
        event_dict = event.to_dict()
        assert event_dict["event_type"] == "sale.created"
        assert event_dict["entity_id"] == "123"
        assert event_dict["data"]["amount"] == 100
    
    @pytest.mark.asyncio
    async def test_event_bus_publish_subscribe(self):
        """Test event bus pub/sub functionality"""
        event_bus = EventBus()
        received_events = []
        
        async def test_handler(event: Event):
            received_events.append(event)
        
        # Subscribe to events
        event_bus.subscribe(EventType.SALE_CREATED, test_handler)
        
        # Publish event
        event = Event(
            event_type=EventType.SALE_CREATED,
            entity_id="123",
            entity_type="sale",
            data={"amount": 100},
            timestamp=datetime.utcnow()
        )
        
        await event_bus.publish(event)
        
        # Verify event was received
        assert len(received_events) == 1
        assert received_events[0].entity_id == "123"
    
    @pytest.mark.asyncio
    async def test_event_store(self):
        """Test event storage functionality"""
        event_bus = EventBus()
        
        event1 = Event(
            event_type=EventType.SALE_CREATED,
            entity_id="123",
            entity_type="sale",
            data={"amount": 100},
            timestamp=datetime.utcnow()
        )
        
        event2 = Event(
            event_type=EventType.CUSTOMER_CREATED,
            entity_id="456",
            entity_type="customer",
            data={"name": "John"},
            timestamp=datetime.utcnow()
        )
        
        await event_bus.publish(event1)
        await event_bus.publish(event2)
        
        # Test get all events
        all_events = event_bus.get_events()
        assert len(all_events) == 2
        
        # Test filter by entity_id
        sale_events = event_bus.get_events(entity_id="123")
        assert len(sale_events) == 1
        assert sale_events[0].entity_type == "sale"
        
        # Test filter by event_type
        customer_events = event_bus.get_events(event_type=EventType.CUSTOMER_CREATED)
        assert len(customer_events) == 1
        assert customer_events[0].entity_id == "456"