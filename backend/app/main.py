from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import engine, Base, get_db
from .core.events import event_bus
from .services.analytics_event_handler import AnalyticsEventHandler
from .api import routes_upload, routes_kpi, routes_admin, sales, customers, expenses, routes_csv_upload, dashboard, data_entry

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize analytics event handler
db = next(get_db())
analytics_handler = AnalyticsEventHandler(db)

# Initialize FastAPI app
app = FastAPI(
    title=settings.project_name,
    description="Analytics API for retail businesses",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc UI
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(routes_upload.router, prefix=settings.api_v1_prefix)
app.include_router(routes_csv_upload.router, prefix=settings.api_v1_prefix)
app.include_router(data_entry.router, prefix=settings.api_v1_prefix)
app.include_router(dashboard.router, prefix=settings.api_v1_prefix)
app.include_router(routes_kpi.router, prefix=settings.api_v1_prefix)
app.include_router(routes_admin.router, prefix=settings.api_v1_prefix)
app.include_router(sales.router, prefix=settings.api_v1_prefix)
app.include_router(customers.router, prefix=settings.api_v1_prefix)
app.include_router(expenses.router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Retail Analytics API",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Detailed health check for monitoring"""
    return {
        "status": "healthy",
        "database": "connected",
        "version": "1.0.0"
    }