import pytest
from datetime import datetime
from app.services.sales_service import SalesService
from app.services.customers_service_v2 import CustomersService
from app.services.kpi_service import KPIService
from app.models.analytics import Sale, Customer, Expense

class TestSalesService:
    
    @pytest.mark.asyncio
    async def test_create_sale(self, db_session):
        """Test sale creation with event emission"""
        service = SalesService(db_session)
        
        sale_data = {
            "product_name": "Test Product",
            "amount": 99.99,
            "customer_id": "CUST001",
            "category": "Electronics",
            "date": datetime.utcnow()
        }
        
        sale = await service.create_sale(sale_data)
        
        assert sale.product_name == "Test Product"
        assert sale.amount_cents == 9999
        assert sale.customer_id == "CUST001"
    
    def test_get_sales(self, db_session):
        """Test sales retrieval with filtering"""
        service = SalesService(db_session)
        
        # Create test sales
        sale1 = Sale(
            product_name="Product 1",
            amount_cents=5000,
            date=datetime.utcnow()
        )
        sale2 = Sale(
            product_name="Product 2",
            amount_cents=7500,
            date=datetime.utcnow()
        )
        
        db_session.add_all([sale1, sale2])
        db_session.commit()
        
        sales = service.get_sales()
        assert len(sales) == 2
    
    @pytest.mark.asyncio
    async def test_update_sale(self, db_session):
        """Test sale update with event emission"""
        service = SalesService(db_session)
        
        # Create initial sale
        sale = Sale(
            product_name="Original Product",
            amount_cents=5000,
            date=datetime.utcnow()
        )
        db_session.add(sale)
        db_session.commit()
        
        # Update sale
        update_data = {"product_name": "Updated Product", "amount": 75.00}
        updated_sale = await service.update_sale(sale.id, update_data)
        
        assert updated_sale.product_name == "Updated Product"
        assert updated_sale.amount_cents == 7500

class TestCustomersService:
    
    @pytest.mark.asyncio
    async def test_create_customer(self, db_session):
        """Test customer creation with event emission"""
        service = CustomersService(db_session)
        
        customer_data = {
            "id": "CUST001",
            "name": "John Doe",
            "email": "john@example.com"
        }
        
        customer = await service.create_customer(customer_data)
        
        assert customer.id == "CUST001"
        assert customer.name == "John Doe"
        assert customer.email == "john@example.com"

class TestKPIService:
    
    def test_get_total_revenue(self, db_session):
        """Test revenue calculation"""
        service = KPIService(db_session)
        
        # Create test sales
        sale1 = Sale(product_name="Product 1", amount_cents=5000, date=datetime.utcnow())
        sale2 = Sale(product_name="Product 2", amount_cents=7500, date=datetime.utcnow())
        
        db_session.add_all([sale1, sale2])
        db_session.commit()
        
        revenue = service.get_total_revenue(30)
        assert revenue == 125.00  # (5000 + 7500) / 100
    
    def test_get_top_products(self, db_session):
        """Test top products calculation"""
        service = KPIService(db_session)
        
        # Create test sales
        sale1 = Sale(product_name="Product A", amount_cents=10000, date=datetime.utcnow())
        sale2 = Sale(product_name="Product B", amount_cents=5000, date=datetime.utcnow())
        sale3 = Sale(product_name="Product A", amount_cents=8000, date=datetime.utcnow())
        
        db_session.add_all([sale1, sale2, sale3])
        db_session.commit()
        
        top_products = service.get_top_products(2)
        
        assert len(top_products) == 2
        assert top_products[0]["product_name"] == "Product A"
        assert top_products[0]["total_revenue"] == 180.00  # (10000 + 8000) / 100
    
    @pytest.mark.asyncio
    async def test_calculate_all_kpis(self, db_session):
        """Test comprehensive KPI calculation"""
        service = KPIService(db_session)
        
        # Create test data
        sale = Sale(product_name="Test Product", amount_cents=10000, date=datetime.utcnow())
        customer = Customer(id="CUST001", name="John Doe")
        expense = Expense(description="Test Expense", amount_cents=2000, date=datetime.utcnow())
        
        db_session.add_all([sale, customer, expense])
        db_session.commit()
        
        kpis = await service.calculate_all_kpis(30)
        
        assert "revenue" in kpis
        assert "profit_margin" in kpis
        assert "top_products" in kpis
        assert "total_customers" in kpis
        assert kpis["revenue"] == 100.00
        assert kpis["total_customers"] == 1