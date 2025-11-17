from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..core.database import get_db
from ..models.schemas import SaleCreate, SaleUpdate, SaleResponse
from ..services.sales_service import SalesService

router = APIRouter(prefix="/sales", tags=["sales"])

@router.post("/", response_model=SaleResponse)
async def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    """Create a new sale record with event emission"""
    service = SalesService(db)
    sale_data = sale.dict()
    db_sale = await service.create_sale(sale_data)
    # Convert cents back to dollars for response
    return SaleResponse(
        id=db_sale.id,
        date=db_sale.date,
        product_name=db_sale.product_name,
        amount=db_sale.amount_cents / 100,
        customer_id=db_sale.customer_id,
        category=db_sale.category,
        created_at=db_sale.created_at
    )

@router.get("/", response_model=List[SaleResponse])
def get_sales(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get sales with optional pagination and date filtering"""
    service = SalesService(db)
    sales = service.get_sales(skip=skip, limit=limit, start_date=start_date, end_date=end_date)
    return [
        SaleResponse(
            id=sale.id,
            date=sale.date,
            product_name=sale.product_name,
            amount=sale.amount_cents / 100,
            customer_id=sale.customer_id,
            category=sale.category,
            created_at=sale.created_at
        )
        for sale in sales
    ]

@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    """Get a specific sale by ID"""
    service = SalesService(db)
    sale = service.get(sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    return SaleResponse(
        id=sale.id,
        date=sale.date,
        product_name=sale.product_name,
        amount=sale.amount_cents / 100,
        customer_id=sale.customer_id,
        category=sale.category,
        created_at=sale.created_at
    )

@router.put("/{sale_id}", response_model=SaleResponse)
async def update_sale(sale_id: int, sale_update: SaleUpdate, db: Session = Depends(get_db)):
    """Update an existing sale with event emission"""
    service = SalesService(db)
    update_data = sale_update.dict(exclude_unset=True)
    sale = await service.update_sale(sale_id, update_data)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    return SaleResponse(
        id=sale.id,
        date=sale.date,
        product_name=sale.product_name,
        amount=sale.amount_cents / 100,
        customer_id=sale.customer_id,
        category=sale.category,
        created_at=sale.created_at
    )

@router.delete("/{sale_id}")
async def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    """Delete a sale with event emission"""
    service = SalesService(db)
    success = await service.delete_sale(sale_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    return {"message": "Sale deleted successfully"}