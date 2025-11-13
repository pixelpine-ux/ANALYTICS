from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services.kpi_service import KPIService

router = APIRouter(prefix="/api/kpis", tags=["KPIs"])

@router.get("/dashboard")
async def get_dashboard_kpis(db: Session = Depends(get_db)):
    """Get all main KPIs for dashboard"""
    kpi_service = KPIService(db)
    
    return {
        "total_revenue": kpi_service.get_total_revenue(),
        "profit_margin": kpi_service.get_profit_margin(),
        "top_products": kpi_service.get_top_products(),
        "repeat_customers": kpi_service.get_repeat_customers()
    }

@router.get("/revenue")
async def get_revenue(days: int = 30, db: Session = Depends(get_db)):
    """Get revenue for specified period"""
    kpi_service = KPIService(db)
    return {"revenue": kpi_service.get_total_revenue(days)}

@router.get("/profit-margin")
async def get_profit_margin(days: int = 30, db: Session = Depends(get_db)):
    """Get profit margin for specified period"""
    kpi_service = KPIService(db)
    return {"profit_margin": kpi_service.get_profit_margin(days)}