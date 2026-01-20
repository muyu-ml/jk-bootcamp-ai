"""FastAPI application entry point."""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import OperationalError, DatabaseError, IntegrityError
from pydantic import ValidationError
import logging

from app.config import settings
from app.api import tickets, tags

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Project Alpha API",
    description="Ticket management system API",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tickets.router, prefix=f"{settings.API_V1_PREFIX}/tickets", tags=["tickets"])
app.include_router(tags.router, prefix=f"{settings.API_V1_PREFIX}/tags", tags=["tags"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors (unique constraints, foreign keys, etc.)."""
    logger.error(f"Database integrity error: {exc}", exc_info=True)
    error_msg = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
    
    # Check for common integrity errors
    if "unique constraint" in error_msg.lower() or "duplicate key" in error_msg.lower():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "A resource with this value already exists.",
                "error": error_msg
            }
        )
    elif "foreign key constraint" in error_msg.lower():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Referenced resource does not exist.",
                "error": error_msg
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Database integrity constraint violation.",
            "error": error_msg
        }
    )


@app.exception_handler(OperationalError)
async def database_operational_error_handler(request: Request, exc: OperationalError):
    """Handle database operational errors (connection issues)."""
    logger.error(f"Database operational error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": "Database connection error. Please check if the database server is running.",
            "error": str(exc)
        }
    )


@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    """Handle general database errors."""
    logger.error(f"Database error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Database error occurred.",
            "error": str(exc)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal server error occurred.",
            "error": str(exc)
        }
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Project Alpha API", "version": "0.1.0"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
