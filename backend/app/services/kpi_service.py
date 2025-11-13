from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from ..models import Sale, Customer, Expense
from datetime import datetime, timedelta
from typing import Dict, List

class KPIService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_total_revenue(self, days: int = 30) -> float:
        """Calculate total revenue for the last N days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = self.db.query(func.sum(Sale.total_amount)).filter(
            Sale.sale_date >= cutoff_date
        ).scalar()
        return result or 0.0
    
    def get_profit_margin(self, days: int = 30) -> float:
        """Calculate profit margin (revenue - expenses) / revenue"""
        revenue = self.get_total_revenue(days)
        if revenue == 0:
            return 0.0
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        expenses = self.db.query(func.sum(Expense.amount)).filter(
            Expense.expense_date >= cutoff_date
        ).scalar() or 0.0
        
        profit = revenue - expenses
        return (profit / revenue) * 100
    
    def get_top_products(self, limit: int = 5) -> List[Dict]:
        """Get top selling products by quantity"""
        results = self.db.query(
            Sale.product_name,
            func.sum(Sale.quantity).label('total_quantity'),
            func.sum(Sale.total_amount).label('total_revenue')
        ).group_by(Sale.product_name).order_by(
            desc('total_quantity')
        ).limit(limit).all()
        
        return [
            {
                "product_name": result.product_name,
                "total_quantity": result.total_quantity,
                "total_revenue": float(result.total_revenue)
            }
            for result in results
        ]
    
    def get_repeat_customers(self) -> int:
        """Count customers with more than one purchase"""
        result = self.db.query(Customer.id).join(Sale).group_by(
            Customer.id
        ).having(func.count(Sale.id) > 1).count()
        return result