from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import datetime, timedelta

from ..core.database import get_db
from ..services.kpi_service import KPIService
from ..services.sales_service import SalesService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/kpis")
async def get_dashboard_kpis(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get all KPIs for dashboard"""
    kpi_service = KPIService(db)
    return await kpi_service.calculate_all_kpis(days)

@router.get("/revenue-trend")
def get_revenue_trend(
    days: int = Query(30, ge=7, le=365),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get daily revenue trend"""
    sales_service = SalesService(db)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get sales grouped by date
    from sqlalchemy import func, Date
    from ..models.analytics import Sale
    
    results = db.query(
        func.date(Sale.date).label('date'),
        func.sum(Sale.amount_cents).label('revenue_cents'),
        func.count(Sale.id).label('transaction_count')
    ).filter(
        Sale.date >= start_date,
        Sale.date <= end_date
    ).group_by(
        func.date(Sale.date)
    ).order_by('date').all()
    
    return [
        {
            "date": result.date.isoformat(),
            "revenue": result.revenue_cents / 100,
            "transactions": result.transaction_count
        }
        for result in results
    ]

@router.get("/customer-analytics")
def get_customer_analytics(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get customer analytics data"""
    from sqlalchemy import func
    from ..models.analytics import Sale, Customer
    
    # Customer purchase frequency
    customer_frequency = db.query(
        Sale.customer_id,
        func.count(Sale.id).label('purchase_count'),
        func.sum(Sale.amount_cents).label('total_spent_cents')
    ).filter(
        Sale.customer_id.isnot(None)
    ).group_by(Sale.customer_id).all()
    
    # Categorize customers
    new_customers = len([c for c in customer_frequency if c.purchase_count == 1])
    repeat_customers = len([c for c in customer_frequency if c.purchase_count > 1])
    vip_customers = len([c for c in customer_frequency if c.total_spent_cents > 50000])  # $500+
    
    return {
        "total_customers": len(customer_frequency),
        "new_customers": new_customers,
        "repeat_customers": repeat_customers,
        "vip_customers": vip_customers,
        "repeat_rate": (repeat_customers / len(customer_frequency) * 100) if customer_frequency else 0
    }

@router.get("/product-performance")
def get_product_performance(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get product performance metrics"""
    kpi_service = KPIService(db)
    return kpi_service.get_top_products(limit)

@router.get("/expense-breakdown")
def get_expense_breakdown(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Get expense breakdown by category"""
    from sqlalchemy import func
    from ..models.analytics import Expense
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    results = db.query(
        Expense.category,
        func.sum(Expense.amount_cents).label('total_cents'),
        func.count(Expense.id).label('expense_count')
    ).filter(
        Expense.date >= cutoff_date
    ).group_by(
        Expense.category
    ).order_by(
        func.sum(Expense.amount_cents).desc()
    ).all()
    
    return [
        {
            "category": result.category or "Uncategorized",
            "total_amount": result.total_cents / 100,
            "expense_count": result.expense_count
        }
        for result in results
    ]