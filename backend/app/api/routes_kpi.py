from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from ..core.database import get_db
from ..services.analytics import AnalyticsService
from ..models.schemas import KPISummary

router = APIRouter(prefix="/kpis", tags=["analytics"])


@router.get("/summary", response_model=KPISummary)
async def get_kpi_summary(
    days_back: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive KPI summary for the specified period
    
    Returns:
    - Total revenue and sales count
    - Average order value
    - Top 5 products by revenue
    - Repeat customers count
    """
    analytics = AnalyticsService(db)
    return analytics.generate_kpi_summary(days_back)


@router.get("/revenue-trend")
async def get_revenue_trend(
    days_back: int = Query(30, ge=1, le=365),
    interval: str = Query("daily", regex="^(daily|weekly|monthly)$"),
    db: Session = Depends(get_db)
):
    """
    Get revenue trend data for charts
    
    Args:
    - days_back: Number of days to analyze
    - interval: Aggregation interval (daily, weekly, monthly)
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days_back)
    
    analytics = AnalyticsService(db)
    trend_data = analytics.get_revenue_trend(start_date, end_date, interval)
    
    return {
        "trend_data": trend_data,
        "period_start": start_date,
        "period_end": end_date,
        "interval": interval
    }


@router.get("/top-products")
async def get_top_products(
    days_back: int = Query(30, ge=1, le=365),
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Get top products by revenue for the specified period
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days_back)
    
    analytics = AnalyticsService(db)
    top_products = analytics.get_top_products(start_date, end_date, limit)
    
    return {
        "top_products": top_products,
        "period_start": start_date,
        "period_end": end_date
    }


@router.get("/summary/custom")
async def get_custom_kpi_summary(
    start_date: datetime = Query(..., description="Start date for analysis"),
    end_date: datetime = Query(..., description="End date for analysis"),
    db: Session = Depends(get_db)
):
    """
    Get KPI summary for custom date range
    """
    analytics = AnalyticsService(db)
    
    revenue_metrics = analytics.calculate_revenue_metrics(start_date, end_date)
    top_products = analytics.get_top_products(start_date, end_date, 5)
    repeat_customers = analytics.count_repeat_customers(start_date, end_date)
    
    return {
        **revenue_metrics,
        "top_products": top_products,
        "repeat_customers_count": repeat_customers,
        "period_start": start_date,
        "period_end": end_date
    }


@router.get("/revenue/comparison")
async def get_revenue_comparison(
    current_days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Compare current period revenue with previous period
    """
    analytics = AnalyticsService(db)
    
    # Current period
    current_end = datetime.utcnow()
    current_start = current_end - timedelta(days=current_days)
    
    # Previous period (same duration)
    previous_end = current_start
    previous_start = previous_end - timedelta(days=current_days)
    
    current_metrics = analytics.calculate_revenue_metrics(current_start, current_end)
    previous_metrics = analytics.calculate_revenue_metrics(previous_start, previous_end)
    
    # Calculate percentage changes
    revenue_change = 0
    if previous_metrics['total_revenue'] > 0:
        revenue_change = ((current_metrics['total_revenue'] - previous_metrics['total_revenue']) / previous_metrics['total_revenue']) * 100
    
    return {
        "current_period": {
            **current_metrics,
            "start_date": current_start,
            "end_date": current_end
        },
        "previous_period": {
            **previous_metrics,
            "start_date": previous_start,
            "end_date": previous_end
        },
        "revenue_change_percent": round(revenue_change, 2)
    }