"""Add performance indexes

Revision ID: perf_001
Revises: b56f21b8eb71
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'perf_001'
down_revision = 'b56f21b8eb71'
branch_labels = None
depends_on = None

def upgrade():
    """
    Performance Optimization Strategy:
    1. Index frequently filtered columns (date ranges)
    2. Index GROUP BY columns (customer_id, category)
    3. Composite indexes for common query patterns
    """
    
    # Sales table indexes - Most critical for analytics
    op.create_index('idx_sales_date', 'sales', ['date'])
    op.create_index('idx_sales_customer_id', 'sales', ['customer_id'])
    op.create_index('idx_sales_product_name', 'sales', ['product_name'])
    
    # Composite index for date range + customer queries (common pattern)
    op.create_index('idx_sales_date_customer', 'sales', ['date', 'customer_id'])
    
    # Expenses table indexes
    op.create_index('idx_expenses_date', 'expenses', ['date'])
    op.create_index('idx_expenses_category', 'expenses', ['category'])
    
    # Customers table indexes
    op.create_index('idx_customers_email', 'customers', ['email'])
    
    print("✅ Performance indexes created successfully")

def downgrade():
    """Remove performance indexes"""
    op.drop_index('idx_sales_date', table_name='sales')
    op.drop_index('idx_sales_customer_id', table_name='sales')
    op.drop_index('idx_sales_product_name', table_name='sales')
    op.drop_index('idx_sales_date_customer', table_name='sales')
    op.drop_index('idx_expenses_date', table_name='expenses')
    op.drop_index('idx_expenses_category', table_name='expenses')
    op.drop_index('idx_customers_email', table_name='customers')