from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import List, Optional
from ..models.analytics import Sale
from ..models.schemas import SaleCreate, SaleUpdate
from fastapi import HTTPException

class SalesService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_sale(self, sale_data: SaleCreate) -> Sale:
        """Create a new sale record"""
        try:
            sale = Sale(
                date=sale_data.date,
                product_name=sale_data.product_name,
                amount_cents=int(sale_data.amount * 100),
                customer_id=sale_data.customer_id,
                category=sale_data.category
            )
            self.db.add(sale)
            self.db.commit()
            self.db.refresh(sale)
            return sale
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error creating sale: {str(e)}")
    
    def get_sale(self, sale_id: int) -> Optional[Sale]:
        """Get sale by ID"""
        return self.db.query(Sale).filter(Sale.id == sale_id).first()
    
    def get_sales(self, skip: int = 0, limit: int = 100, 
                  start_date: Optional[datetime] = None,
                  end_date: Optional[datetime] = None) -> List[Sale]:
        """Get sales with optional date filtering"""
        query = self.db.query(Sale)
        
        if start_date:
            query = query.filter(Sale.date >= start_date)
        if end_date:
            query = query.filter(Sale.date <= end_date)
            
        return query.order_by(desc(Sale.date)).offset(skip).limit(limit).all()
    
    def update_sale(self, sale_id: int, sale_data: SaleUpdate) -> Optional[Sale]:
        """Update existing sale"""
        try:
            sale = self.get_sale(sale_id)
            if not sale:
                return None
            
            update_data = sale_data.dict(exclude_unset=True)
            if 'amount' in update_data:
                update_data['amount_cents'] = int(update_data.pop('amount') * 100)
            
            for field, value in update_data.items():
                setattr(sale, field, value)
            
            self.db.commit()
            self.db.refresh(sale)
            return sale
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error updating sale: {str(e)}")
    
    def delete_sale(self, sale_id: int) -> bool:
        """Delete sale by ID"""
        try:
            sale = self.get_sale(sale_id)
            if not sale:
                return False
            
            self.db.delete(sale)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error deleting sale: {str(e)}")