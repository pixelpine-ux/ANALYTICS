import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Dict, Tuple
from ..models.analytics import Sale
from io import StringIO


class DataProcessor:
    """
    Handles CSV processing with robust error handling and validation
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def process_csv_content(self, csv_content: str) -> Tuple[int, List[str]]:
        """
        Algorithm: Batch processing with validation
        Data Structure: List for errors (append-only), DataFrame for bulk operations
        
        Returns: (records_processed, errors_list)
        """
        errors = []
        records_processed = 0
        
        try:
            # Use pandas for efficient CSV parsing
            df = pd.read_csv(StringIO(csv_content))
            
            # Validate required columns
            required_columns = ['date', 'product_name', 'amount']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                errors.append(f"Missing required columns: {', '.join(missing_columns)}")
                return 0, errors
            
            # Process in batches for better memory management
            batch_size = 1000
            sales_to_add = []
            
            for index, row in df.iterrows():
                try:
                    # Validate and convert each row
                    sale_data = self._validate_row(row, index)
                    if sale_data:
                        sales_to_add.append(Sale(**sale_data))
                        
                        # Batch insert when we reach batch_size
                        if len(sales_to_add) >= batch_size:
                            self._bulk_insert_sales(sales_to_add)
                            records_processed += len(sales_to_add)
                            sales_to_add = []
                            
                except Exception as e:
                    errors.append(f"Row {index + 2}: {str(e)}")  # +2 for header and 0-indexing
            
            # Insert remaining records
            if sales_to_add:
                self._bulk_insert_sales(sales_to_add)
                records_processed += len(sales_to_add)
            
        except Exception as e:
            errors.append(f"CSV parsing error: {str(e)}")
        
        return records_processed, errors
    
    def _validate_row(self, row: pd.Series, row_index: int) -> Dict:
        """
        Data validation with detailed error messages
        Algorithm: Early return on validation failure
        """
        try:
            # Parse date with multiple format support
            date_str = str(row['date']).strip()
            try:
                # Try common date formats
                for date_format in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
                    try:
                        parsed_date = datetime.strptime(date_str, date_format)
                        break
                    except ValueError:
                        continue
                else:
                    raise ValueError(f"Invalid date format: {date_str}")
            except ValueError as e:
                raise ValueError(f"Date parsing error: {e}")
            
            # Validate amount
            try:
                amount = float(row['amount'])
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                amount_cents = int(amount * 100)  # Convert to cents
            except (ValueError, TypeError):
                raise ValueError(f"Invalid amount: {row['amount']}")
            
            # Clean product name
            product_name = str(row['product_name']).strip()
            if not product_name or product_name.lower() == 'nan':
                raise ValueError("Product name is required")
            
            # Optional fields with defaults
            customer_id = str(row.get('customer_id', '')).strip() or None
            category = str(row.get('category', '')).strip() or None
            
            return {
                'date': parsed_date,
                'product_name': product_name,
                'amount_cents': amount_cents,
                'customer_id': customer_id,
                'category': category
            }
            
        except Exception as e:
            raise ValueError(str(e))
    
    def _bulk_insert_sales(self, sales: List[Sale]) -> None:
        """
        Bulk insert for performance
        Algorithm: Single transaction for batch
        """
        try:
            self.db.bulk_save_objects(sales)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e