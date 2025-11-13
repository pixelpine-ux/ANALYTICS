from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, index=True)  # Index for time-series queries
    product_name = Column(String, nullable=False)
    amount_cents = Column(Integer, nullable=False)  # Store as cents to avoid float issues
    customer_id = Column(String, nullable=True, index=True)  # Index for repeat customer analysis
    category = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Composite index for common queries
    __table_args__ = (
        Index('ix_sales_date_customer', 'date', 'customer_id'),
    )


class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(String, primary_key=True)  # External customer ID
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, index=True)
    description = Column(String, nullable=False)
    amount_cents = Column(Integer, nullable=False)
    category = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)