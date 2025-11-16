from fastapi import HTTPException
from typing import Optional

class AnalyticsException(Exception):
    """Base exception for analytics application"""
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class ValidationError(AnalyticsException):
    """Raised when data validation fails"""
    pass

class NotFoundError(AnalyticsException):
    """Raised when requested resource is not found"""
    pass

class DuplicateError(AnalyticsException):
    """Raised when trying to create duplicate resource"""
    pass

class DatabaseError(AnalyticsException):
    """Raised when database operation fails"""
    pass

def handle_service_exceptions(func):
    """Decorator to convert service exceptions to HTTP exceptions"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.message)
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=e.message)
        except DuplicateError as e:
            raise HTTPException(status_code=409, detail=e.message)
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    return wrapper
