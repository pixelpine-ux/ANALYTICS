import pytest
from datetime import datetime
from app.core.events import EventType, event_bus
from app.services.sales_service import SalesService
from app.services.analytics_event_handler import AnalyticsEventHandler

class TestEventIntegration:
    
    @pytest.mark.asyncio
    async def test_sale_creation_triggers_kpi_recalculation(self, db_session):
        """Test that creating a sale triggers KPI recalculation"""
        # Setup event handler
        analytics_handler = AnalyticsEventHandler(db_session)
        
        # Track KPI events
        kpi_events = []
        
        async def kpi_event_tracker(event):
            kpi_events.append(event)
        
        event_bus.subscribe(EventType.KPI_CALCULATED, kpi_event_tracker)
        
        # Create a sale
        sales_service = SalesService(db_session)
        sale_data = {
            "product_name": "Test Product",
            "amount": 99.99,
            "date": datetime.utcnow()
        }
        
        await sales_service.create_sale(sale_data)
        
        # Verify KPI event was emitted
        assert len(kpi_events) > 0
        assert kpi_events[0].event_type == EventType.KPI_CALCULATED
    
    @pytest.mark.asyncio
    async def test_end_to_end_data_flow(self, db_session):
        """Test complete data flow from entry to analytics"""
        # Setup analytics handler
        analytics_handler = AnalyticsEventHandler(db_session)
        
        # Track all events
        all_events = []
        
        async def event_tracker(event):
            all_events.append(event)
        
        # Subscribe to all event types
        for event_type in EventType:
            event_bus.subscribe(event_type, event_tracker)
        
        # Create sales service
        sales_service = SalesService(db_session)
        
        # Create multiple sales
        sales_data = [
            {"product_name": "Product A", "amount": 50.00, "date": datetime.utcnow()},
            {"product_name": "Product B", "amount": 75.00, "date": datetime.utcnow()},
            {"product_name": "Product A", "amount": 60.00, "date": datetime.utcnow()}
        ]
        
        for sale_data in sales_data:
            await sales_service.create_sale(sale_data)
        
        # Verify events were generated
        sale_events = [e for e in all_events if e.event_type == EventType.SALE_CREATED]
        kpi_events = [e for e in all_events if e.event_type == EventType.KPI_CALCULATED]
        
        assert len(sale_events) == 3
        assert len(kpi_events) >= 3  # At least one KPI event per sale
        
        # Verify data integrity
        from app.services.kpi_service import KPIService
        kpi_service = KPIService(db_session)
        
        revenue = kpi_service.get_total_revenue(30)
        assert revenue == 185.00  # 50 + 75 + 60
        
        top_products = kpi_service.get_top_products(2)
        assert len(top_products) == 2
        assert top_products[0]["product_name"] == "Product A"  # Higher total revenue

class TestAPIIntegration:
    
    def test_dashboard_data_consistency(self, client, db_session):
        """Test that dashboard APIs return consistent data"""
        # Create test data via API
        sale_data = {
            "product_name": "Integration Test Product",
            "amount": 100.00,
            "customer_id": "CUST001",
            "category": "Test",
            "date": datetime.utcnow().isoformat()
        }
        
        # Create sale
        response = client.post("/api/v1/sales/", json=sale_data)
        assert response.status_code == 200
        
        # Get KPIs
        kpi_response = client.get("/api/v1/dashboard/kpis?days=30")
        assert kpi_response.status_code == 200
        kpi_data = kpi_response.json()
        
        # Get revenue trend
        trend_response = client.get("/api/v1/dashboard/revenue-trend?days=7")
        assert trend_response.status_code == 200
        trend_data = trend_response.json()
        
        # Get product performance
        product_response = client.get("/api/v1/dashboard/product-performance?limit=5")
        assert product_response.status_code == 200
        product_data = product_response.json()
        
        # Verify consistency
        assert kpi_data["revenue"] >= 100.00
        assert len(product_data) >= 1
        assert product_data[0]["product_name"] == "Integration Test Product"
    
    def test_data_entry_to_analytics_flow(self, client):
        """Test complete flow from data entry to analytics"""
        # Step 1: Create customer
        customer_data = {
            "id": "INTEGRATION_CUST",
            "name": "Integration Test Customer",
            "email": "test@integration.com"
        }
        
        customer_response = client.post("/api/v1/entry/quick-customer", json=customer_data)
        assert customer_response.status_code == 200
        
        # Step 2: Create sales
        sales_data = [
            {
                "product_name": "Integration Product A",
                "amount": 50.00,
                "customer_id": "INTEGRATION_CUST",
                "category": "Test"
            },
            {
                "product_name": "Integration Product B",
                "amount": 75.00,
                "customer_id": "INTEGRATION_CUST",
                "category": "Test"
            }
        ]
        
        for sale_data in sales_data:
            sale_response = client.post("/api/v1/entry/quick-sale", json=sale_data)
            assert sale_response.status_code == 200
        
        # Step 3: Verify analytics
        kpi_response = client.get("/api/v1/dashboard/kpis?days=30")
        assert kpi_response.status_code == 200
        kpi_data = kpi_response.json()
        
        customer_analytics_response = client.get("/api/v1/dashboard/customer-analytics")
        assert customer_analytics_response.status_code == 200
        customer_analytics = customer_analytics_response.json()
        
        # Verify data
        assert kpi_data["revenue"] >= 125.00  # 50 + 75
        assert customer_analytics["total_customers"] >= 1
        assert customer_analytics["repeat_customers"] >= 1  # Customer made 2 purchases

class TestErrorHandling:
    
    def test_invalid_data_handling(self, client):
        """Test API error handling with invalid data"""
        # Test invalid sale data
        invalid_sale = {
            "product_name": "",  # Empty product name
            "amount": -10.00,    # Negative amount
        }
        
        response = client.post("/api/v1/entry/quick-sale", json=invalid_sale)
        assert response.status_code == 400
    
    def test_missing_resource_handling(self, client):
        """Test handling of missing resources"""
        # Test getting non-existent sale
        response = client.get("/api/v1/sales/99999")
        assert response.status_code == 404
        
        # Test updating non-existent sale
        update_data = {"product_name": "Updated Product"}
        response = client.put("/api/v1/sales/99999", json=update_data)
        assert response.status_code == 404