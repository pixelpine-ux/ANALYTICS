import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from io import StringIO
from .sales_service import SalesService
from .customers_service_v2 import CustomersService
from .expenses_service_v2 import ExpensesService

class CSVUploadService:
    """Service for handling CSV uploads with validation and bulk operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.sales_service = SalesService(db)
        self.customers_service = CustomersService(db)
        self.expenses_service = ExpensesService(db)
    
    async def upload_sales_csv(self, file: UploadFile) -> Dict[str, Any]:
        """Upload and process sales CSV file"""
        try:
            # Read CSV content
            content = await file.read()
            df = pd.read_csv(StringIO(content.decode('utf-8')))
            
            # Validate required columns
            required_columns = ['date', 'product_name', 'amount']
            self._validate_columns(df, required_columns)
            
            # Process and validate data
            processed_data = []
            errors = []
            
            for index, row in df.iterrows():
                try:
                    sale_data = self._process_sale_row(row)
                    processed_data.append(sale_data)
                except Exception as e:
                    errors.append(f"Row {index + 1}: {str(e)}")
            
            # If there are validation errors, return them
            if errors:
                return {
                    "success": False,
                    "errors": errors,
                    "processed_count": 0,
                    "total_rows": len(df)
                }
            
            # Bulk insert with events
            created_sales = []
            for sale_data in processed_data:
                sale = await self.sales_service.create_sale(sale_data)
                created_sales.append(sale)
            
            return {
                "success": True,
                "processed_count": len(created_sales),
                "total_rows": len(df),
                "errors": []
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")
    
    async def upload_customers_csv(self, file: UploadFile) -> Dict[str, Any]:
        """Upload and process customers CSV file"""
        try:
            content = await file.read()
            df = pd.read_csv(StringIO(content.decode('utf-8')))
            
            required_columns = ['id', 'name']
            self._validate_columns(df, required_columns)
            
            processed_data = []
            errors = []
            
            for index, row in df.iterrows():
                try:
                    customer_data = self._process_customer_row(row)
                    processed_data.append(customer_data)
                except Exception as e:
                    errors.append(f"Row {index + 1}: {str(e)}")
            
            if errors:
                return {
                    "success": False,
                    "errors": errors,
                    "processed_count": 0,
                    "total_rows": len(df)
                }
            
            created_customers = []
            for customer_data in processed_data:
                customer = await self.customers_service.create_customer(customer_data)
                created_customers.append(customer)
            
            return {
                "success": True,
                "processed_count": len(created_customers),
                "total_rows": len(df),
                "errors": []
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")
    
    async def upload_expenses_csv(self, file: UploadFile) -> Dict[str, Any]:
        """Upload and process expenses CSV file"""
        try:
            content = await file.read()
            df = pd.read_csv(StringIO(content.decode('utf-8')))
            
            required_columns = ['date', 'description', 'amount']
            self._validate_columns(df, required_columns)
            
            processed_data = []
            errors = []
            
            for index, row in df.iterrows():
                try:
                    expense_data = self._process_expense_row(row)
                    processed_data.append(expense_data)
                except Exception as e:
                    errors.append(f"Row {index + 1}: {str(e)}")
            
            if errors:
                return {
                    "success": False,
                    "errors": errors,
                    "processed_count": 0,
                    "total_rows": len(df)
                }
            
            created_expenses = []
            for expense_data in processed_data:
                expense = await self.expenses_service.create_expense(expense_data)
                created_expenses.append(expense)
            
            return {
                "success": True,
                "processed_count": len(created_expenses),
                "total_rows": len(df),
                "errors": []
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")
    
    def _validate_columns(self, df: pd.DataFrame, required_columns: List[str]):
        """Validate that required columns exist in DataFrame"""
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
    
    def _process_sale_row(self, row: pd.Series) -> Dict[str, Any]:
        """Process and validate a single sale row"""
        return {
            "date": pd.to_datetime(row['date']),
            "product_name": str(row['product_name']).strip(),
            "amount": float(row['amount']),
            "customer_id": str(row.get('customer_id', '')).strip() or None,
            "category": str(row.get('category', '')).strip() or None
        }
    
    def _process_customer_row(self, row: pd.Series) -> Dict[str, Any]:
        """Process and validate a single customer row"""
        return {
            "id": str(row['id']).strip(),
            "name": str(row['name']).strip(),
            "email": str(row.get('email', '')).strip() or None
        }
    
    def _process_expense_row(self, row: pd.Series) -> Dict[str, Any]:
        """Process and validate a single expense row"""
        return {
            "date": pd.to_datetime(row['date']),
            "description": str(row['description']).strip(),
            "amount": float(row['amount']),
            "category": str(row.get('category', '')).strip() or None
        }