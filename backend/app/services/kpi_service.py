from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from ..models.analytics import Sale, Customer, Expense
from ..core.events import Event, EventType, event_bus
from ..core.cache import cached, cache_invalidate
from datetime import datetime, timedelta
from typing import Dict, List, Any

class KPIService:
    def __init__(self, db: Session):
        self.db = db
    
    @cached("kpi_summary", ttl_seconds=300)  # Cache for 5 minutes
    async def calculate_all_kpis(self, days: int = 30) -> Dict[str, Any]:
        """Calculate all KPIs and emit event - CACHED VERSION"""
        kpis = {
            "revenue": self.get_total_revenue(days),
            "profit_margin": self.get_profit_margin(days),
            "top_products": self.get_top_products(),
            "repeat_customers": self.get_repeat_customers(),
            "total_customers": self.get_total_customers(),
            "avg_order_value": self.get_avg_order_value(days),
            "calculated_at": datetime.utcnow().isoformat(),
            "period_days": days
        }
        
        # Emit KPI calculated event
        await self._emit_kpi_event(kpis)
        return kpis
    
    @cached("revenue", ttl_seconds=180)  # Cache for 3 minutes
    def get_total_revenue(self, days: int = 30) -> float:
        """Calculate total revenue for the last N days - CACHED"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = self.db.query(func.sum(Sale.amount_cents)).filter(
            Sale.date >= cutoff_date
        ).scalar()
        return (result or 0) / 100  # Convert cents to dollars
    
    def get_profit_margin(self, days: int = 30) -> float:
        """Calculate profit margin (revenue - expenses) / revenue"""
        revenue = self.get_total_revenue(days)
        if revenue == 0:
            return 0.0
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        expenses = self.db.query(func.sum(Expense.amount_cents)).filter(
            Expense.date >= cutoff_date
        ).scalar() or 0
        
        expenses_dollars = expenses / 100
        profit = revenue - expenses_dollars
        return (profit / revenue) * 100
    
    @cached("top_products", ttl_seconds=600)  # Cache for 10 minutes
    def get_top_products(self, limit: int = 5) -> List[Dict]:
        """Get top selling products by revenue - CACHED"""
        results = self.db.query(
            Sale.product_name,
            func.count(Sale.id).label('total_sales'),
            func.sum(Sale.amount_cents).label('total_revenue_cents')
        ).group_by(Sale.product_name).order_by(
            desc('total_revenue_cents')
        ).limit(limit).all()
        
        return [
            {
                "product_name": result.product_name,
                "total_sales": result.total_sales,
                "total_revenue": result.total_revenue_cents / 100
            }
            for result in results
        ]
    
    def get_repeat_customers(self) -> int:
        """Count customers with more than one purchase"""
        result = self.db.query(Sale.customer_id).filter(
            Sale.customer_id.isnot(None)
        ).group_by(Sale.customer_id).having(
            func.count(Sale.id) > 1
        ).count()
        return result
    
    def get_total_customers(self) -> int:
        """Get total unique customers"""
        return self.db.query(Customer).count()
    
    def get_avg_order_value(self, days: int = 30) -> float:
        """Calculate average order value"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = self.db.query(func.avg(Sale.amount_cents)).filter(
            Sale.date >= cutoff_date
        ).scalar()
        return (result or 0) / 100
    
    async def _emit_kpi_event(self, kpis: Dict[str, Any]):
        """Emit KPI calculated event"""
        event = Event(
            event_type=EventType.KPI_CALCULATED,
            entity_id=f"kpi_{datetime.utcnow().isoformat()}",
            entity_type="kpi",
            data=kpis,
            timestamp=datetime.utcnow()
        )
        await event_bus.publish(event)