from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List


class SaleCreate(BaseModel):
    date: datetime
    product_name: str
    amount: float  # API accepts float, we convert to cents internally
    customer_id: Optional[str] = None
    category: Optional[str] = None
    
    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v


class SaleResponse(BaseModel):
    id: int
    date: datetime
    product_name: str
    amount: float  # Convert back from cents for API response
    customer_id: Optional[str]
    category: Optional[str]
    
    class Config:
        from_attributes = True


class KPISummary(BaseModel):
    total_revenue: float
    total_sales_count: int
    average_order_value: float
    top_products: List[dict]
    repeat_customers_count: int
    period_start: datetime
    period_end: datetime


class UploadResponse(BaseModel):
    message: str
    records_processed: int
    errors: List[str] = []