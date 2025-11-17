"""
Simple test script to verify the event-driven architecture works
"""
import asyncio
from datetime import datetime
from core.events import Event, EventType, event_bus

# Test event handler
async def test_event_handler(event: Event):
    print(f"Received event: {event.event_type.value}")
    print(f"Entity: {event.entity_type} (ID: {event.entity_id})")
    print(f"Data: {event.data}")
    print(f"Timestamp: {event.timestamp}")
    print("---")

async def test_event_system():
    """Test the event system"""
    print("Testing Event-Driven Architecture...")
    
    # Subscribe to events
    event_bus.subscribe(EventType.SALE_CREATED, test_event_handler)
    event_bus.subscribe(EventType.KPI_CALCULATED, test_event_handler)
    
    # Create test events
    sale_event = Event(
        event_type=EventType.SALE_CREATED,
        entity_id="123",
        entity_type="sale",
        data={
            "product_name": "Test Product",
            "amount_cents": 2999,
            "customer_id": "CUST001"
        },
        timestamp=datetime.utcnow()
    )
    
    kpi_event = Event(
        event_type=EventType.KPI_CALCULATED,
        entity_id="revenue_kpi_001",
        entity_type="kpi",
        data={
            "kpi_type": "revenue",
            "value": 15000.50,
            "period": "monthly"
        },
        timestamp=datetime.utcnow()
    )
    
    # Publish events
    await event_bus.publish(sale_event)
    await event_bus.publish(kpi_event)
    
    # Check event store
    print(f"Total events in store: {len(event_bus.get_events())}")
    print("Event system test completed!")

if __name__ == "__main__":
    asyncio.run(test_event_system())