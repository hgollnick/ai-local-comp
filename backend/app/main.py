"""
Main FastAPI application.
"""
try:
    import debugpy
    DEBUGPY_AVAILABLE = True
except ImportError:
    DEBUGPY_AVAILABLE = False

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import router as v1_router
from app.schemas.common import ErrorResponse, StatusResponse


# Setup logging
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    logger.info(f"Starting {settings.app_name}")
    logger.info(f"Debug mode: {settings.debug}")
    
    # Setup debugpy if in debug mode
    if settings.debug and DEBUGPY_AVAILABLE:
        try:
            debugpy.listen(("0.0.0.0", 5678))
            logger.info("Debugpy is listening on 0.0.0.0:5678")
        except Exception as e:
            logger.warning(f"Could not start debugpy: {e}")
    elif settings.debug and not DEBUGPY_AVAILABLE:
        logger.warning("Debug mode enabled but debugpy not available")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI Local Comp Backend API",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(v1_router, prefix="/api/v1")

# Legacy API support (if needed)
# app.include_router(v1_router, prefix="/api")  # Uncomment for backward compatibility


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc) if settings.debug else "An unexpected error occurred"
        ).dict()
    )


@app.get("/", response_model=StatusResponse)
async def root() -> StatusResponse:
    """Root endpoint with service information."""
    return StatusResponse(
        status="running",
        message=f"Welcome to {settings.app_name} v1.0.0 - API available at /api/v1/"
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
