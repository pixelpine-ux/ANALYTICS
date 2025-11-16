from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from ..models.analytics import Customer
from ..models.schemas import CustomerCreate, CustomerUpdate
from fastapi import HTTPException

class CustomersService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_customer(self, customer_data: CustomerCreate) -> Customer:
        """Create a new customer"""
        try:
            existing = self.get_customer(customer_data.id)
            if existing:
                raise HTTPException(status_code=400, detail="Customer ID already exists")
            
            customer = Customer(
                id=customer_data.id,
                name=customer_data.name,
                email=customer_data.email
            )
            self.db.add(customer)
            self.db.commit()
            self.db.refresh(customer)
            return customer
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error creating customer: {str(e)}")
    
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID"""
        return self.db.query(Customer).filter(Customer.id == customer_id).first()
    
    def get_customers(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        """Get all customers with pagination"""
        return self.db.query(Customer).order_by(desc(Customer.created_at)).offset(skip).limit(limit).all()
    
    def update_customer(self, customer_id: str, customer_data: CustomerUpdate) -> Optional[Customer]:
        """Update existing customer"""
        try:
            customer = self.get_customer(customer_id)
            if not customer:
                return None
            
            update_data = customer_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(customer, field, value)
            
            self.db.commit()
            self.db.refresh(customer)
            return customer
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error updating customer: {str(e)}")
    
    def delete_customer(self, customer_id: str) -> bool:
        """Delete customer by ID"""
        try:
            customer = self.get_customer(customer_id)
            if not customer:
                return False
            
            self.db.delete(customer)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error deleting customer: {str(e)}")