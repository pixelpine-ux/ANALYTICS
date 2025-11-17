import pytest
from datetime import datetime
from app.models.analytics import Sale, Customer, Expense

class TestDashboardAPI:
    
    def test_get_kpis(self, client, db_session):
        """Test KPIs endpoint"""
        # Create test data
        sale = Sale(product_name="Test Product", amount_cents=10000, date=datetime.utcnow())
        db_session.add(sale)
        db_session.commit()
        
        response = client.get("/api/v1/dashboard/kpis?days=30")
        
        assert response.status_code == 200
        data = response.json()
        assert "revenue" in data
        assert "profit_margin" in data
        assert "top_products" in data
    
    def test_get_revenue_trend(self, client, db_session):
        """Test revenue trend endpoint"""
        # Create test sales
        sale1 = Sale(product_name="Product 1", amount_cents=5000, date=datetime.utcnow())
        sale2 = Sale(product_name="Product 2", amount_cents=7500, date=datetime.utcnow())
        
        db_session.add_all([sale1, sale2])
        db_session.commit()
        
        response = client.get("/api/v1/dashboard/revenue-trend?days=7")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:  # If there's data
            assert "date" in data[0]
            assert "revenue" in data[0]
            assert "transactions" in data[0]
    
    def test_get_customer_analytics(self, client, db_session):
        """Test customer analytics endpoint"""
        # Create test data
        customer = Customer(id="CUST001", name="John Doe")
        sale1 = Sale(product_name="Product 1", amount_cents=5000, customer_id="CUST001", date=datetime.utcnow())
        sale2 = Sale(product_name="Product 2", amount_cents=7500, customer_id="CUST001", date=datetime.utcnow())
        
        db_session.add_all([customer, sale1, sale2])
        db_session.commit()
        
        response = client.get("/api/v1/dashboard/customer-analytics")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_customers" in data
        assert "repeat_customers" in data
        assert "repeat_rate" in data

class TestDataEntryAPI:
    
    def test_quick_sale_entry(self, client):
        """Test quick sale entry endpoint"""
        sale_data = {
            "product_name": "Test Product",
            "amount": 99.99,
            "customer_id": "CUST001",
            "category": "Electronics"
        }
        
        response = client.post("/api/v1/entry/quick-sale", json=sale_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "sale_id" in data
    
    def test_quick_customer_entry(self, client):
        """Test quick customer entry endpoint"""
        customer_data = {
            "id": "CUST001",
            "name": "John Doe",
            "email": "john@example.com"
        }
        
        response = client.post("/api/v1/entry/quick-customer", json=customer_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "customer_id" in data
    
    def test_quick_expense_entry(self, client):
        """Test quick expense entry endpoint"""
        expense_data = {
            "description": "Office supplies",
            "amount": 45.50,
            "category": "Operations"
        }
        
        response = client.post("/api/v1/entry/quick-expense", json=expense_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "expense_id" in data
    
    def test_product_suggestions(self, client, db_session):
        """Test product suggestions endpoint"""
        # Create test sales with products
        sale1 = Sale(product_name="Widget A", amount_cents=5000, date=datetime.utcnow())
        sale2 = Sale(product_name="Widget B", amount_cents=7500, date=datetime.utcnow())
        
        db_session.add_all([sale1, sale2])
        db_session.commit()
        
        response = client.get("/api/v1/entry/suggestions/products?query=Widget")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert "Widget A" in data
        assert "Widget B" in data

class TestSalesAPI:
    
    def test_create_sale(self, client):
        """Test sale creation via API"""
        sale_data = {
            "product_name": "Test Product",
            "amount": 99.99,
            "customer_id": "CUST001",
            "category": "Electronics",
            "date": datetime.utcnow().isoformat()
        }
        
        response = client.post("/api/v1/sales/", json=sale_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["product_name"] == "Test Product"
        assert data["amount"] == 99.99
    
    def test_get_sales(self, client, db_session):
        """Test sales retrieval via API"""
        # Create test sale
        sale = Sale(product_name="Test Product", amount_cents=9999, date=datetime.utcnow())
        db_session.add(sale)
        db_session.commit()
        
        response = client.get("/api/v1/sales/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["product_name"] == "Test Product"

class TestHealthCheck:
    
    def test_root_endpoint(self, client):
        """Test root health check"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
    
    def test_health_endpoint(self, client):
        """Test detailed health check"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"