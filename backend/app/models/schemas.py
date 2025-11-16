from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

# === SALES SCHEMAS ===
class SaleCreate(BaseModel):
    date: datetime
    product_name: str = Field(..., min_length=1, max_length=200)
    amount: float = Field(..., gt=0, description="Amount in dollars")
    customer_id: Optional[str] = Field(None, max_length=50)
    category: Optional[str] = Field(None, max_length=100)
    
    @validator('product_name')
    def validate_product_name(cls, v):
        if not v.strip():
            raise ValueError('Product name cannot be empty')
        return v.strip()
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        if v > 999999.99:
            raise ValueError('Amount too large')
        return round(v, 2)

class SaleUpdate(BaseModel):
    date: Optional[datetime] = None
    product_name: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[float] = Field(None, gt=0)
    customer_id: Optional[str] = Field(None, max_length=50)
    category: Optional[str] = Field(None, max_length=100)

class SaleResponse(BaseModel):
    id: int
    date: datetime
    product_name: str
    amount: float
    customer_id: Optional[str]
    category: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# === CUSTOMER SCHEMAS ===
class CustomerCreate(BaseModel):
    id: str = Field(..., min_length=1, max_length=50)
    name: Optional[str] = Field(None, max_length=200)
    email: Optional[str] = Field(None, max_length=255)
    
    @validator('id')
    def validate_customer_id(cls, v):
        if not v.strip():
            raise ValueError('Customer ID cannot be empty')
        return v.strip().upper()
    
    @validator('email')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Invalid email format')
        return v

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    email: Optional[str] = Field(None, max_length=255)

class CustomerResponse(BaseModel):
    id: str
    name: Optional[str]
    email: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# === EXPENSE SCHEMAS ===
class ExpenseCreate(BaseModel):
    date: datetime
    description: str = Field(..., min_length=1, max_length=500)
    amount: float = Field(..., gt=0, description="Amount in dollars")
    category: Optional[str] = Field(None, max_length=100)
    
    @validator('description')
    def validate_description(cls, v):
        if not v.strip():
            raise ValueError('Description cannot be empty')
        return v.strip()
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return round(v, 2)

class ExpenseUpdate(BaseModel):
    date: Optional[datetime] = None
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, max_length=100)

class ExpenseResponse(BaseModel):
    id: int
    date: datetime
    description: str
    amount: float
    category: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# === ANALYTICS SCHEMAS ===
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

# === ERROR SCHEMAS ===
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# === BULK OPERATIONS ===
class BulkSaleCreate(BaseModel):
    sales: List[SaleCreate] = Field(..., max_items=1000)

class BulkResponse(BaseModel):
    success_count: int
    error_count: int
    errors: List[str] = []

# === UTILITY FUNCTIONS ===
def convert_sale_to_response(sale) -> SaleResponse:
    """Convert Sale model to SaleResponse schema"""
    return SaleResponse(
        id=sale.id,
        date=sale.date,
        product_name=sale.product_name,
        amount=sale.amount_cents / 100,
        customer_id=sale.customer_id,
        category=sale.category,
        created_at=sale.created_at
    )

def convert_expense_to_response(expense) -> ExpenseResponse:
    """Convert Expense model to ExpenseResponse schema"""
    return ExpenseResponse(
        id=expense.id,
        date=expense.date,
        description=expense.description,
        amount=expense.amount_cents / 100,
        category=expense.category,
        created_at=expense.created_at
    )
