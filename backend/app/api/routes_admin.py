from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..core.database import get_db
from ..services.sheets_connector import GoogleSheetsConnector, SheetsURLParser
from ..services.pdf_generator import PDFReportGenerator
from ..models.schemas import UploadResponse
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["admin"])


# Pydantic models for admin operations
class BusinessSettings(BaseModel):
    business_name: str
    revenue_goal_monthly: Optional[float] = None
    target_customers_monthly: Optional[int] = None
    
class SheetsConnection(BaseModel):
    spreadsheet_url: str
    sheet_name: Optional[str] = "Sheet1"
    
class ReportRequest(BaseModel):
    days_back: int = 30
    business_name: str = "Your Business"
    include_charts: bool = True


@router.post("/connect-sheets", response_model=UploadResponse)
async def connect_google_sheets(
    connection: SheetsConnection,
    db: Session = Depends(get_db)
):
    """
    Connect to Google Sheets and import data
    
    Senior Engineer Note: Always validate external URLs and handle auth gracefully
    """
    try:
        # Validate and extract spreadsheet ID
        spreadsheet_id = SheetsURLParser.extract_spreadsheet_id(connection.spreadsheet_url)
        
        if not spreadsheet_id:
            raise HTTPException(
                status_code=400, 
                detail="Invalid Google Sheets URL. Please provide a valid spreadsheet URL."
            )
        
        # Initialize connector
        connector = GoogleSheetsConnector(db)
        
        # Test connection first
        validation_result = connector.validate_sheet_access(spreadsheet_id)
        
        if not validation_result["valid"]:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot access spreadsheet: {validation_result['error']}"
            )
        
        # Import data
        records_processed, errors = connector.extract_sheet_data(
            spreadsheet_id, 
            connection.sheet_name
        )
        
        return UploadResponse(
            message=f"Successfully imported {records_processed} records from '{validation_result['title']}'",
            records_processed=records_processed,
            errors=errors
        )
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@router.get("/validate-sheets")
async def validate_sheets_connection(
    url: str = Query(..., description="Google Sheets URL to validate")
):
    """
    Validate Google Sheets connection without importing data
    
    Use case: Frontend can check if URL is valid before showing import button
    """
    try:
        spreadsheet_id = SheetsURLParser.extract_spreadsheet_id(url)
        
        if not spreadsheet_id:
            return {
                "valid": False,
                "error": "Invalid URL format",
                "suggestion": "URL should look like: https://docs.google.com/spreadsheets/d/YOUR_ID/edit"
            }
        
        # Test connection
        connector = GoogleSheetsConnector(None)  # No DB needed for validation
        result = connector.validate_sheet_access(spreadsheet_id)
        
        return result
        
    except Exception as e:
        return {"valid": False, "error": str(e)}


@router.post("/generate-pdf-report")
async def generate_pdf_report(
    request: ReportRequest,
    db: Session = Depends(get_db)
):
    """
    Generate PDF report for download
    
    Algorithm: Generate PDF in memory, return as downloadable response
    """
    try:
        generator = PDFReportGenerator(db)
        pdf_bytes = generator.generate_kpi_report(
            days_back=request.days_back,
            business_name=request.business_name
        )
        
        # In a real app, you'd return a FastAPI Response with PDF content
        # For now, return metadata about the generated report
        return {
            "success": True,
            "report_size_bytes": len(pdf_bytes),
            "filename": f"analytics_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            "generated_at": datetime.utcnow().isoformat(),
            "message": "PDF report generated successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


@router.post("/create-public-link")
async def create_public_dashboard_link(
    request: ReportRequest,
    db: Session = Depends(get_db)
):
    """
    Create a public shareable dashboard link
    
    Security consideration: No sensitive data, time-limited access
    """
    try:
        generator = PDFReportGenerator(db)
        public_link_data = generator.generate_public_report_link(
            days_back=request.days_back,
            business_name=request.business_name
        )
        
        return {
            "success": True,
            "public_url": public_link_data["public_url"],
            "report_id": public_link_data["report_id"],
            "expires_at": public_link_data["expires_at"],
            "message": "Public dashboard link created successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Public link creation failed: {str(e)}")


@router.get("/business-settings")
async def get_business_settings():
    """
    Get current business settings and goals
    
    In production: Store in database, implement user authentication
    """
    # Mock settings for MVP
    return {
        "business_name": "Your Retail Store",
        "revenue_goal_monthly": 10000.00,
        "target_customers_monthly": 500,
        "currency": "USD",
        "timezone": "UTC",
        "last_updated": datetime.utcnow().isoformat()
    }


@router.put("/business-settings")
async def update_business_settings(
    settings: BusinessSettings
):
    """
    Update business settings and goals
    
    Senior Engineer Note: In production, add validation, audit logging, and user auth
    """
    try:
        # Validation
        if settings.revenue_goal_monthly and settings.revenue_goal_monthly < 0:
            raise HTTPException(status_code=400, detail="Revenue goal must be positive")
        
        if settings.target_customers_monthly and settings.target_customers_monthly < 0:
            raise HTTPException(status_code=400, detail="Customer target must be positive")
        
        # In production: Save to database
        # For MVP: Return success with the updated settings
        
        return {
            "success": True,
            "message": "Business settings updated successfully",
            "settings": settings.dict(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Settings update failed: {str(e)}")


@router.get("/system-status")
async def get_system_status(db: Session = Depends(get_db)):
    """
    System health check for admin monitoring
    
    Use case: Admin dashboard can show system health
    """
    try:
        # Test database connection
        db.execute("SELECT 1").fetchone()
        db_status = "healthy"
        
        # Check recent data
        from ..models.analytics import Sale
        recent_sales = db.query(Sale).count()
        
        return {
            "status": "healthy",
            "database": db_status,
            "total_sales_records": recent_sales,
            "last_check": datetime.utcnow().isoformat(),
            "version": "1.0.0"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "last_check": datetime.utcnow().isoformat()
        }


@router.delete("/clear-data")
async def clear_all_data(
    confirm: bool = Query(False, description="Must be true to confirm deletion"),
    db: Session = Depends(get_db)
):
    """
    Clear all sales data (for testing/demo purposes)
    
    Senior Engineer Warning: Extremely dangerous operation!
    In production: Require admin authentication, audit logging, backup confirmation
    """
    if not confirm:
        raise HTTPException(
            status_code=400, 
            detail="Data deletion requires explicit confirmation. Set confirm=true"
        )
    
    try:
        from ..models.analytics import Sale, Customer, Expense
        
        # Count records before deletion
        sales_count = db.query(Sale).count()
        customers_count = db.query(Customer).count()
        expenses_count = db.query(Expense).count()
        
        # Delete all data
        db.query(Sale).delete()
        db.query(Customer).delete()
        db.query(Expense).delete()
        db.commit()
        
        return {
            "success": True,
            "message": "All data cleared successfully",
            "deleted_records": {
                "sales": sales_count,
                "customers": customers_count,
                "expenses": expenses_count
            },
            "cleared_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Data clearing failed: {str(e)}")