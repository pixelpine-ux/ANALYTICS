from datetime import datetime
from sqlalchemy.orm import Session
from ..core.events import Event, EventType, event_bus
from .kpi_service import KPIService

class AnalyticsEventHandler:
    """Handles analytics-related events and triggers KPI recalculation"""
    
    def __init__(self, db: Session):
        self.db = db
        self.kpi_service = KPIService(db)
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """Subscribe to relevant events"""
        # Sales events trigger KPI recalculation
        event_bus.subscribe(EventType.SALE_CREATED, self.handle_sales_change)
        event_bus.subscribe(EventType.SALE_UPDATED, self.handle_sales_change)
        event_bus.subscribe(EventType.SALE_DELETED, self.handle_sales_change)
        
        # Expense events trigger profit margin recalculation
        event_bus.subscribe(EventType.EXPENSE_CREATED, self.handle_expense_change)
        event_bus.subscribe(EventType.EXPENSE_UPDATED, self.handle_expense_change)
        
        # Customer events for repeat customer analysis
        event_bus.subscribe(EventType.CUSTOMER_CREATED, self.handle_customer_change)
        event_bus.subscribe(EventType.CUSTOMER_UPDATED, self.handle_customer_change)
    
    async def handle_sales_change(self, event: Event):
        """Handle sales-related events"""
        try:
            # Trigger KPI recalculation
            await self._recalculate_sales_kpis()
            
            # Emit KPI calculated event
            await self._emit_kpi_calculated_event("sales_kpis", event.entity_id)
            
        except Exception as e:
            print(f"Error handling sales change event: {e}")
    
    async def handle_expense_change(self, event: Event):
        """Handle expense-related events"""
        try:
            # Trigger profit margin recalculation
            await self._recalculate_profit_margins()
            
            # Emit KPI calculated event
            await self._emit_kpi_calculated_event("profit_margins", event.entity_id)
            
        except Exception as e:
            print(f"Error handling expense change event: {e}")
    
    async def handle_customer_change(self, event: Event):
        """Handle customer-related events"""
        try:
            # Trigger customer analytics recalculation
            await self._recalculate_customer_analytics()
            
            # Emit KPI calculated event
            await self._emit_kpi_calculated_event("customer_analytics", event.entity_id)
            
        except Exception as e:
            print(f"Error handling customer change event: {e}")
    
    async def _recalculate_sales_kpis(self):
        """Recalculate sales-related KPIs"""
        await self.kpi_service.calculate_all_kpis()
    
    async def _recalculate_profit_margins(self):
        """Recalculate profit margins"""
        await self.kpi_service.calculate_all_kpis()
    
    async def _recalculate_customer_analytics(self):
        """Recalculate customer analytics"""
        await self.kpi_service.calculate_all_kpis()
    
    async def _emit_kpi_calculated_event(self, kpi_type: str, trigger_entity_id: str):
        """Emit event when KPIs are recalculated"""
        kpi_event = Event(
            event_type=EventType.KPI_CALCULATED,
            entity_id=f"{kpi_type}_{datetime.utcnow().isoformat()}",
            entity_type="kpi",
            data={
                "kpi_type": kpi_type,
                "trigger_entity_id": trigger_entity_id,
                "calculated_at": datetime.utcnow().isoformat()
            },
            timestamp=datetime.utcnow()
        )
        await event_bus.publish(kpi_event)