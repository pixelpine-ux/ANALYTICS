from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from ..models.analytics import Sale, Customer
from collections import defaultdict


class AnalyticsService:
    """
    Senior Engineer Principle: Keep business logic separate from API logic.
    This service contains pure analytics functions that can be tested independently.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_revenue_metrics(self, start_date: datetime, end_date: datetime) -> Dict:
        """
        Algorithm: Single-pass aggregation with SQL optimization
        Data Structure: Dictionary for O(1) lookups
        """
        # Use SQL aggregation instead of Python loops - much faster for large datasets
        revenue_query = self.db.query(
            func.sum(Sale.amount_cents).label('total_cents'),
            func.count(Sale.id).label('total_sales'),
            func.avg(Sale.amount_cents).label('avg_cents')
        ).filter(
            Sale.date >= start_date,
            Sale.date <= end_date
        ).first()
        
        total_cents = revenue_query.total_cents or 0
        total_sales = revenue_query.total_sales or 0
        avg_cents = revenue_query.avg_cents or 0
        
        return {
            'total_revenue': total_cents / 100,  # Convert back to dollars
            'total_sales_count': total_sales,
            'average_order_value': avg_cents / 100 if avg_cents else 0
        }
    
    def get_top_products(self, start_date: datetime, end_date: datetime, limit: int = 5) -> List[Dict]:
        """
        Algorithm: SQL GROUP BY with ORDER BY - database does the heavy lifting
        Why this approach: Let the database engine optimize the sorting
        """
        top_products = self.db.query(
            Sale.product_name,
            func.sum(Sale.amount_cents).label('total_revenue_cents'),
            func.count(Sale.id).label('sales_count')
        ).filter(
            Sale.date >= start_date,
            Sale.date <= end_date
        ).group_by(
            Sale.product_name
        ).order_by(
            desc('total_revenue_cents')
        ).limit(limit).all()
        
        return [
            {
                'product_name': product.product_name,
                'total_revenue': product.total_revenue_cents / 100,
                'sales_count': product.sales_count
            }
            for product in top_products
        ]
    
    def count_repeat_customers(self, start_date: datetime, end_date: datetime) -> int:
        """
        Algorithm: SQL subquery to count customers with multiple purchases
        Data Structure: Set operations handled by database
        """
        # Find customers who made more than 1 purchase in the period
        repeat_customers = self.db.query(
            Sale.customer_id,
            func.count(Sale.id).label('purchase_count')
        ).filter(
            Sale.date >= start_date,
            Sale.date <= end_date,
            Sale.customer_id.isnot(None)  # Only count identified customers
        ).group_by(
            Sale.customer_id
        ).having(
            func.count(Sale.id) > 1
        ).count()
        
        return repeat_customers
    
    def get_revenue_trend(self, start_date: datetime, end_date: datetime, 
                         interval: str = 'daily') -> List[Dict]:
        """
        Algorithm: Time-series aggregation with date truncation
        Performance: Single query instead of multiple date range queries
        """
        if interval == 'daily':
            date_trunc = func.date(Sale.date)
        elif interval == 'weekly':
            # SQLite doesn't have date_trunc, so we use a simpler approach
            date_trunc = func.strftime('%Y-%W', Sale.date)
        else:  # monthly
            date_trunc = func.strftime('%Y-%m', Sale.date)
        
        trend_data = self.db.query(
            date_trunc.label('period'),
            func.sum(Sale.amount_cents).label('revenue_cents')
        ).filter(
            Sale.date >= start_date,
            Sale.date <= end_date
        ).group_by(
            date_trunc
        ).order_by(
            date_trunc
        ).all()
        
        return [
            {
                'period': str(row.period),
                'revenue': row.revenue_cents / 100
            }
            for row in trend_data
        ]
    
    def generate_kpi_summary(self, days_back: int = 30) -> Dict:
        """
        Master function that combines all KPIs
        Performance optimization: Single service instance, multiple optimized queries
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days_back)
        
        # Combine all metrics in one response
        revenue_metrics = self.calculate_revenue_metrics(start_date, end_date)
        top_products = self.get_top_products(start_date, end_date)
        repeat_customers = self.count_repeat_customers(start_date, end_date)
        
        return {
            **revenue_metrics,
            'top_products': top_products,
            'repeat_customers_count': repeat_customers,
            'period_start': start_date,
            'period_end': end_date
        }