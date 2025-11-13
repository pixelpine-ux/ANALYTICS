from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services.data_processor import DataProcessor
from ..models.schemas import UploadResponse

router = APIRouter(prefix="/upload", tags=["data-upload"])


@router.post("/csv", response_model=UploadResponse)
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload CSV file with sales data
    
    Expected CSV format:
    - date (YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY)
    - product_name (required)
    - amount (positive number)
    - customer_id (optional)
    - category (optional)
    """
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        # Read file content
        content = await file.read()
        csv_content = content.decode('utf-8')
        
        # Process the data
        processor = DataProcessor(db)
        records_processed, errors = processor.process_csv_content(csv_content)
        
        return UploadResponse(
            message=f"Successfully processed {records_processed} records",
            records_processed=records_processed,
            errors=errors
        )
        
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.get("/sample-csv")
async def get_sample_csv():
    """
    Download a sample CSV file for reference
    """
    sample_data = """date,product_name,amount,customer_id,category
2024-01-15,Coffee,5.99,CUST001,beverages
2024-01-15,Sandwich,8.50,CUST002,food
2024-01-16,Coffee,5.99,CUST001,beverages"""
    
    return {"sample_csv": sample_data}