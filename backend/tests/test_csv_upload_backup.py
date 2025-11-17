import pytest
from io import BytesIO
from fastapi import UploadFile
from app.services.csv_upload_service import CSVUploadService

class TestCSVUploadService:
    
    @pytest.mark.asyncio
    async def test_upload_sales_csv_success(self, db_session):
        """Test successful sales CSV upload"""
        service = CSVUploadService(db_session)
        
        # Create test CSV content
        csv_content = """date,product_name,amount,customer_id,category
2024-01-15,Widget A,29.99,CUST001,Electronics
2024-01-16,Widget B,45.50,CUST002,Electronics"""
        
        # Create mock file
        file_obj = BytesIO(csv_content.encode())
        upload_file = UploadFile(filename="test_sales.csv", file=file_obj)
        
        result = await service.upload_sales_csv(upload_file)
        
        assert result["success"] is True
        assert result["processed_count"] == 2
        assert result["total_rows"] == 2
        assert len(result["errors"]) == 0
    
    @pytest.mark.asyncio
    async def test_upload_sales_csv_validation_errors(self, db_session):
        """Test CSV upload with validation errors"""
        service = CSVUploadService(db_session)
        
        # Create CSV with invalid data
        csv_content = """date,product_name,amount,customer_id,category
invalid-date,Widget A,29.99,CUST001,Electronics
2024-01-16,Widget B,invalid-amount,CUST002,Electronics"""
        
        file_obj = BytesIO(csv_content.encode())
        upload_file = UploadFile(filename="test_sales.csv", file=file_obj)
        
        result = await service.upload_sales_csv(upload_file)
        
        assert result["success"] is False
        assert result["processed_count"] == 0
        assert len(result["errors"]) > 0
    
    @pytest.mark.asyncio
    async def test_upload_customers_csv_success(self, db_session):
        """Test successful customers CSV upload"""
        service = CSVUploadService(db_session)
        
        csv_content = """id,name,email
CUST001,John Doe,john@example.com
CUST002,Jane Smith,jane@example.com"""
        
        file_obj = BytesIO(csv_content.encode())
        upload_file = UploadFile(filename="test_customers.csv", file=file_obj)
        
        result = await service.upload_customers_csv(upload_file)
        
        assert result["success"] is True
        assert result["processed_count"] == 2
        assert result["total_rows"] == 2
    
    @pytest.mark.asyncio
    async def test_upload_expenses_csv_success(self, db_session):
        """Test successful expenses CSV upload"""
        service = CSVUploadService(db_session)
        
        csv_content = """date,description,amount,category
2024-01-15,Office supplies,45.50,Operations
2024-01-16,Marketing materials,125.00,Marketing"""
        
        file_obj = BytesIO(csv_content.encode())
        upload_file = UploadFile(filename="test_expenses.csv", file=file_obj)
        
        result = await service.upload_expenses_csv(upload_file)
        
        assert result["success"] is True
        assert result["processed_count"] == 2
        assert result["total_rows"] == 2
    
    def test_validate_columns_success(self, db_session):
        """Test successful column validation"""
        service = CSVUploadService(db_session)
        
        import pandas as pd
        df = pd.DataFrame({
            'date': ['2024-01-15'],
            'product_name': ['Widget A'],
            'amount': [29.99]
        })
        
        required_columns = ['date', 'product_name', 'amount']
        
        # Should not raise exception
        service._validate_columns(df, required_columns)
    
    def test_validate_columns_missing(self, db_session):
        """Test column validation with missing columns"""
        service = CSVUploadService(db_session)
        
        import pandas as pd
        df = pd.DataFrame({
            'date': ['2024-01-15'],
            'product_name': ['Widget A']
            # Missing 'amount' column
        })
        
        required_columns = ['date', 'product_name', 'amount']
        
        with pytest.raises(ValueError, match="Missing required columns"):
            service._validate_columns(df, required_columns)
    
    def test_process_sale_row(self, db_session):
        """Test sale row processing"""
        service = CSVUploadService(db_session)
        
        import pandas as pd
        row = pd.Series({
            'date': '2024-01-15',
            'product_name': 'Widget A',
            'amount': 29.99,
            'customer_id': 'CUST001',
            'category': 'Electronics'
        })
        
        result = service._process_sale_row(row)
        
        assert result['product_name'] == 'Widget A'
        assert result['amount'] == 29.99
        assert result['customer_id'] == 'CUST001'
        assert result['category'] == 'Electronics'

class TestCSVUploadAPI:
    
    def test_upload_sales_csv_endpoint(self, client):
        """Test sales CSV upload endpoint"""
        csv_content = """date,product_name,amount,customer_id,category
2024-01-15,Widget A,29.99,CUST001,Electronics"""
        
        files = {"file": ("test_sales.csv", csv_content, "text/csv")}
        response = client.post("/api/v1/data/upload-sales-csv", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
    
    def test_upload_invalid_file_type(self, client):
        """Test upload with invalid file type"""
        files = {"file": ("test.txt", "invalid content", "text/plain")}
        response = client.post("/api/v1/data/upload-sales-csv", files=files)
        
        assert response.status_code == 400
        data = response.json()
        assert "File must be a CSV" in data["detail"]
    
    def test_get_csv_template(self, client):
        """Test CSV template endpoint"""
        response = client.get("/api/v1/data/upload-template/sales")
        
        assert response.status_code == 200
        data = response.json()
        assert "columns" in data
        assert "example" in data
        assert "date" in data["columns"]
        assert "product_name" in data["columns"]
    
    def test_get_invalid_template(self, client):
        """Test invalid template request"""
        response = client.get("/api/v1/data/upload-template/invalid")
        
        assert response.status_code == 404
        data = response.json()
        assert "Template not found" in data["detail"]