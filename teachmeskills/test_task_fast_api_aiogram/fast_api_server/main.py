import redis.asyncio as aioredis
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from starlette.status import HTTP_401_UNAUTHORIZED

from database import engine
from logger import logger  # Logger for logging important events
from models import Base

from src.auth.services import router as auth_router
from src.notes.services import router as notes_router
from src.notes_web.services import router as notes_web_router, templates

app = FastAPI()

# Register API routes
app.include_router(auth_router, prefix="/api/v1")
app.include_router(notes_router, prefix="/api/v1")
app.include_router(notes_web_router)

# Mount static files for serving CSS, JS, images, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")


# Exception handler for HTTP exceptions
@app.exception_handler(HTTPException)
async def api_http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions differently for API and web routes."""
    if request.url.path.startswith("/api/v1"):
        # Log the exception details for debugging API issues
        logger.warning(f"API exception occurred at {request.url.path}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    else:
        if exc.status_code == HTTP_401_UNAUTHORIZED:
            # Redirect unauthorized users to the login page
            logger.info("Unauthorized access attempt, redirecting to login.")
            return RedirectResponse(url="/login")
        # Handle exceptions for web routes with a template response
        return templates.TemplateResponse("error.html", {"request": request, "detail": exc.detail},
                                          status_code=exc.status_code)


# Global exception handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Log and handle any uncaught exceptions globally."""
    # Log the error with stack trace for easier debugging
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."},
    )


# Startup event for initializing resources
@app.on_event("startup")
async def startup():
    """Initialize database and Redis on application startup."""
    # Log the startup event
    logger.info("Starting application, initializing database and Redis...")

    # Create all tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Initialize Redis for rate limiting
    redis = aioredis.from_url("redis://redis", encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis)

    # Log successful startup
    logger.info("Application startup complete, database and Redis initialized.")
