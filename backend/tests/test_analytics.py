import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..app.core.database import Base
from ..app.models.analytics import Sale
from ..app.services.analytics import AnalyticsService

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_sales(db_session):
    """Create sample sales data for testing"""
    sales_data = [
        Sale(
            date=datetime(2024, 1, 15),
            product_name="Coffee",
            amount_cents=599,  # $5.99
            customer_id="CUST001"
        ),
        Sale(
            date=datetime(2024, 1, 16),
            product_name="Coffee",
            amount_cents=599,
            customer_id="CUST001"  # Repeat customer
        ),
        Sale(
            date=datetime(2024, 1, 17),
            product_name="Sandwich",
            amount_cents=850,  # $8.50
            customer_id="CUST002"
        )
    ]
    
    for sale in sales_data:
        db_session.add(sale)
    db_session.commit()
    
    return sales_data


def test_revenue_calculation(db_session, sample_sales):
    """Test basic revenue calculation"""
    analytics = AnalyticsService(db_session)
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 31)
    
    metrics = analytics.calculate_revenue_metrics(start_date, end_date)
    
    # Expected: $5.99 + $5.99 + $8.50 = $20.48
    assert metrics['total_revenue'] == 20.48
    assert metrics['total_sales_count'] == 3
    assert metrics['average_order_value'] == pytest.approx(6.83, rel=1e-2)


def test_top_products(db_session, sample_sales):
    """Test top products calculation"""
    analytics = AnalyticsService(db_session)
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 31)
    
    top_products = analytics.get_top_products(start_date, end_date, limit=2)
    
    # Coffee should be #1 with $11.98 (2 sales)
    assert len(top_products) == 2
    assert top_products[0]['product_name'] == 'Coffee'
    assert top_products[0]['total_revenue'] == 11.98
    assert top_products[0]['sales_count'] == 2


def test_repeat_customers(db_session, sample_sales):
    """Test repeat customer identification"""
    analytics = AnalyticsService(db_session)
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 31)
    
    repeat_count = analytics.count_repeat_customers(start_date, end_date)
    
    # Only CUST001 made multiple purchases
    assert repeat_count == 1