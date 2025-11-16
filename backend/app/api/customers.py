from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..models.schemas import CustomerCreate, CustomerUpdate, CustomerResponse
from ..services.customers_service import CustomersService

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer"""
    service = CustomersService(db)
    return service.create_customer(customer)

@router.get("/", response_model=List[CustomerResponse])
def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get customers with pagination"""
    service = CustomersService(db)
    return service.get_customers(skip=skip, limit=limit)

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    """Get a specific customer by ID"""
    service = CustomersService(db)
    customer = service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: str, customer_update: CustomerUpdate, db: Session = Depends(get_db)):
    """Update an existing customer"""
    service = CustomersService(db)
    customer = service.update_customer(customer_id, customer_update)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    """Delete a customer"""
    service = CustomersService(db)
    success = service.delete_customer(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {"message": "Customer deleted successfully"}